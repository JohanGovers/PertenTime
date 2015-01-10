$(document).ready(function(){
	var vm = new RegistrationVm();

	$.get('get_time_entries',{startDate: '2015-01-01', endDate: '2015-01-31'}, function(projects){
		for (var i = 0; i < projects.length; i++) {
			vm.projects.push(new Project(projects[i].id, projects[i].name, projects[i].timeentries));
		}
		
		ko.applyBindings(vm);
	});
})