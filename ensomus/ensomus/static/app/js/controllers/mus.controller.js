controllers.controller('musController', ['$scope', '$timeout', 'QuestionnaireService', function ($scope, $timeout, QuestionnaireService) {
	$scope.privateText = '';

	$scope.init = function(questionnaireUserId, isPrivate, isMine) {
		$scope.questionnaireUserId = questionnaireUserId;
		QuestionnaireService.get(questionnaireUserId).then(function(response) {
			$scope.index = 0;
			$scope.showDescription = true;
			$scope.questionnaire = response.data;
			$scope.expandCollapse = 'icon-chevron-down';
			$scope.updateButtonVisibility();
		});
		$scope.isPrivate = isPrivate;
		$scope.isMine = isMine;
		
	};

	$scope.toggleIsPrivate = function() {
		QuestionnaireService.toggleIsPrivate($scope.questionnaireUserId).then(function(response) {
			$scope.isPrivate = !$scope.isPrivate;
			//$scope.privateText = $scope.isPrivate ? 'Gør synlig for din leder' : 'Skjul for din leder';
		});
	};

	$scope.toogleDescriptions = function() {
		$scope.showDescription = !$scope.showDescription;
		$scope.expandCollapse = $scope.showDescription ? 'icon-chevron-up': 'icon-chevron-down';
		return false;
	};

	$scope.forward = function() {
		$scope.index++;
		$scope.updateButtonVisibility();
		jq('html,body').scrollTop(0);
	};

	$scope.rewind = function() {
		$scope.index--;
		$scope.updateButtonVisibility();
		jq('html,body').scrollTop(0);
	};

	$scope.updateButtonVisibility = function() {
		$scope.first = $scope.index == 0;
		$scope.last = $scope.index == $scope.questionnaire.length - 1;
	};

	$scope.answerKeyUp = function(event, question) {
		question.changed = question.response != question.new_response;
		if (question.changed) {
			if (question.autoSavePromise) {
				$timeout.cancel(question.autoSavePromise);
			}
			question.autoSavePromise = $timeout(function save() {
	        	QuestionnaireService.saveQuestion($scope.questionnaireUserId, question);
	    	},1000);
		}
	};

	$scope.end = function() {
		var questions = [];
		angular.forEach($scope.questionnaire, function(entry, key) {
            angular.forEach(entry.questions, function(question, index) {
                questions.push(question);
            });
        });
		QuestionnaireService.saveQuestions($scope.questionnaireUserId, questions);
	};

	$scope.$watch('isPrivate', function(value) {
		var text = $scope.isMine ? 'leder' : 'medarbejder';
		$scope.privateText = (value ? 'Gør synlig for din ' : 'Skjul for din ') + text;
	});
}]);