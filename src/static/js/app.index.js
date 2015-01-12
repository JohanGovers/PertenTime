$(document).ready(function(){
	var vm = new RegistrationVm();

	vm.loadData();
	
	ko.applyBindings(vm);
})