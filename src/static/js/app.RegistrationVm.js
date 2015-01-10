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
	
	self.projects = ko.observableArray();
}
