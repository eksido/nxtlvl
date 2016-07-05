controllers.controller('developmentPlanCompetenceIntroController', ['$scope', '$timeout','$rootScope', function ($scope, $timeout,$rootScope) {
	$scope.getCompetenceFieldCount = function() {
		return $scope.getCompetenceFields().length;
	}
	$scope.getCompetenceFields = function() {
		var cfs = [];
		for (var i=3,il=$rootScope.states.length-2;i<il;i++) {
			cfs.push({name: $rootScope.states[i].name})
		}
		return cfs;
	}
}]);