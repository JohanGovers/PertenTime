function TimeEntry(projectId, date, hours, submitted) {
	var self = this;
	
	self.projectId = projectId;
	self.date = date;
	self.hours = ko.observable(hours);
	self.submitted = ko.observable(submitted);
	
	self.hours.subscribe(function(newValue){
		$.ajax({
			type: 'POST',
			url: 'save_time_entry',
			data: { projectId: self.projectId, date: self.date, hours: self.hours() },
			})
			//.done(function(data){
			//	console.log(data);
			//})
			.fail(function(req, status, error){
				// TODO: Show some error message in the UI.
				console.error(status, error, "Something went wrong when saving.", self, "Hours: " + self.hours() );
			});
	});
}

function Project(id, name, timeentries) {
	var self = this;
	
	self.id = id;
	self.name = name;
	
	self.timeentries = ko.observableArray(timeentries.map(function(entry){
		return new TimeEntry(id, entry.date, entry.hours, entry.submitted);
	}));
}

function RegistrationVm() {
	var self = this;
	
	self.dataLoadingInProgress = ko.observable(false);
	
	self.startDate = moment().startOf('isoWeek');
	self.endDate = moment().endOf('isoWeek').hours(0).minutes(0).seconds(0).milliseconds(0);
	self.submittedUntil = undefined;
	self.projects = ko.observableArray();
	
	self.allSubmitted = ko.observable(false);
	
	
	self.loadData = function(){
		if(!self.dataLoadingInProgress()) {
			self.dataLoadingInProgress(true);
			$.get('get_time_entries', { startDate: self.startDate.format("YYYY-MM-DD"), endDate: self.endDate.format("YYYY-MM-DD") }, function(data){
				self.projects.removeAll();
				self.submittedUntil = moment(data.submittedUntil);
				self.allSubmitted(self.endDate <= self.submittedUntil);
				for (var i = 0; i < data.projects.length; i++) {
					self.projects.push(new Project(data.projects[i].id, data.projects[i].name, data.projects[i].timeentries));
				}
				
				self.dataLoadingInProgress(false);
			});
		}
	}
	
	self.loadNextWeek = function () {
		self.startDate = self.startDate.add(7, 'days');
		self.endDate = self.endDate.add(7, 'days');
		
		self.loadData();
	}
	
	self.loadPreviousWeek = function () {
		self.startDate = self.startDate.subtract(7, 'days');
		self.endDate = self.endDate.subtract(7, 'days');
		
		self.loadData();
	}
	
	self.submitUntilCurrentWeek = function () {
		var submitEndDate;
		if (self.startDate.month() != self.endDate.month()) {
			if (self.submittedUntil.isBetween(self.startDate, self.endDate, 'day')) {
				submitEndDate = self.endDate.format("YYYY-MM-DD");
			} else {
				submitEndDate = self.startDate.endOf('month').format("YYYY-MM-DD");
			}
		} else {
			submitEndDate = self.endDate.format("YYYY-MM-DD");
		}
		$.ajax({
			type: 'POST',
			url: 'set_last_submitted',
			data: { date: submitEndDate },
			})
			.done(function(data){
				console.log(data);
				self.loadData();
			})
			.fail(function(req, status, error){
				// TODO: Show some error message in the UI.
				console.error(status, error, "Something went wrong when submitting.", self);
			});
	}
}
