function TimeEntry(projectId, date, hours) {
	var self = this;
	
	self.projectId = projectId;
	self.date = date;
	self.hours = ko.observable(hours);
	
	self.hours.subscribe(function(newValue){
		$.ajax({
			type: 'POST',
			url: 'create_time_post',
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
		return new TimeEntry(id, entry.date, entry.hours);
	}));
}

function RegistrationVm() {
	var self = this;
	
	self.startDate = moment().startOf('isoWeek');
	self.endDate = moment().endOf('isoWeek');
	self.projects = ko.observableArray();
	
	self.loadData = function(){
		$.get('get_time_entries', { startDate: self.startDate.format("YYYY-MM-DD"), endDate: self.endDate.format("YYYY-MM-DD") }, function(projects){
			self.projects.removeAll();
			for (var i = 0; i < projects.length; i++) {
				self.projects.push(new Project(projects[i].id, projects[i].name, projects[i].timeentries));
			}
		});
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
}
