"use strict";

function TimeEntry(projectId, date, hours, submitted, vm) {
	var self = this;
	
	self.projectId = projectId;
	self.date = date;
	self.hasError = ko.observable(false);
	self.hours = ko.observable(hours).extend({ rateLimit: { timeout: 400, method: "notifyWhenChangesStop" } });
	self.submitted = ko.observable(submitted);
	
	self.hours.subscribe(function(){
		//Sanitize input of time.
		var value = self.hours();
		
		var value = self.hours().replace(',', '.');
	
		//No non numeric characters.
		value = value.replace(/[^\d.$]/g, '');
		
		//Only one decimal point
		if ((value.match(/\./g) || []).length > 1) {
			var idxFirstDot = value.indexOf('.');  
			var idxSecondDot = value.indexOf('.', idxFirstDot + 1);
			value = value.substring(0, idxSecondDot);
		}
		
		//Allow only 2 decimals
		if ((value.split('.')[1] || []).length > 2){
			value = Number(value).toFixed(2);
		}
		
		self.hours(value);
			
		$.ajax({
			type: 'POST',
			url: 'save_time_entry',
			data: { projectId: self.projectId, date: self.date, hours: self.hours() },
			})
			.done(function(data){
				self.hasError(false);
				vm.savedAt("Saved at " + new Date().toLocaleTimeString());
			})
			.fail(function(req, status, error){
				self.hasError(true);
				vm.logError(status, error);
		});
	});
}

function Project(id, code, name, timeentries, vm) {
	var self = this;
	
	self.id = id;
	self.code = code;
	self.name = name;
	
	self.timeentries = ko.observableArray(timeentries.map(function(entry){
		return new TimeEntry(id, entry.date, entry.hours, entry.submitted, vm);
	}));
}

function RegistrationVm() {
	var self = this;
	
	self.savedAt = ko.observable();
	self.dataLoadingInProgress = ko.observable(false);
	self.showErrorMessage = ko.observable(false);
	self.logError = function(status, error){
		console.error(status, error, "Something went wrong when submitting.", self);
		self.showErrorMessage(true);
	};
	
	self.startDate = ko.observable();
	self.endDate = ko.observable();
	self.submittedUntil = ko.observable();
	self.projects = ko.observableArray();
	
	self.allSubmitted = ko.observable(false);
	
	self.totalHours = ko.computed(function(){
		var sum = 0;
		var projects = self.projects();
		for(var i = 0; i < projects.length; i++){
			var timeentries = projects[i].timeentries();
			for (var j = 0; j < timeentries.length; j++) {
				var val = parseInt(timeentries[j].hours());
				if (isFinite(val)) {
					sum += val;
				}
			}
		}
		
		return sum;
	});
	self.disableSubmitButton = ko.computed(function(){
		return self.dataLoadingInProgress() || self.endDate() <= self.submittedUntil();
	});
	
	self.loadData = function(){
		if(!self.dataLoadingInProgress()) {
			self.dataLoadingInProgress(true);
			var requestData = {};
			if (!!self.startDate()) {
				requestData = { startDate: self.startDate().format("YYYY-MM-DD") }
			}
			
			$.ajax({
				type: 'GET',
				url: 'get_time_entries',
				data: requestData,
			})
			.done(function(data){
				self.projects.removeAll();
				self.submittedUntil(moment(data.submittedUntil));
				self.startDate(moment(data.startDate));
				self.endDate(moment(data.endDate));
				self.allSubmitted(self.endDate() <= self.submittedUntil());
				for (var i = 0; i < data.projects.length; i++) {
					self.projects.push(new Project(data.projects[i].id, data.projects[i].code, data.projects[i].name, data.projects[i].timeentries, self));
				}
				
				self.dataLoadingInProgress(false);
			})
			.fail(function(req, status, error){
				self.logError(status, error);
			});
		}
	}
	
	self.loadNextWeek = function () {
		if (!self.allSubmitted()) {
			return;
		}
		self.startDate(self.startDate().add(7, 'days'));
		self.endDate(self.endDate().add(7, 'days'));
		
		self.loadData();
	}
	
	self.loadPreviousWeek = function () {
		self.startDate(self.startDate().subtract(7, 'days'));
		self.endDate(self.endDate().subtract(7, 'days'));
		
		self.loadData();
	}
	
	self.submitUntilCurrentWeek = function () {
		$.ajax({
			type: 'POST',
			url: 'set_last_submitted',
			data: { date: self.endDate().format("YYYY-MM-DD") },
			})
			.done(function(data){
				self.startDate(null);
				self.loadData();
			})
			.fail(function(req, status, error){
				self.logError(status, error);
			});
	}
}
