controllers.controller('developmentPlanProgressbarController', [
	'$scope', 
	'$rootScope',
	'$timeout',
	'$location',
	'DevelopmentPlanService', 
	function ($scope, $rootScope, $timeout,$location,DevelopmentPlanService) {
	$rootScope.states = [];
	$rootScope.LANGUAGE_CODE = LANGUAGE_CODE;
	$rootScope.trans = trans;
	$rootScope.owner_name = owner_name;
	DevelopmentPlanService.getStatesFuture(developmentplan_user_id).then(function (response) {
		$rootScope.states = response.data;
		var c = 0;
		for (var i=0,ilen=$rootScope.states.length;i<ilen;i++) {
			for (var j=0,jlen=$rootScope.states[i].status.length;j<jlen;j++) {
				c++;
			}
		}
		$scope.size = c;
		var i =0;
		angular.forEach($rootScope.states,function (state) {
			angular.forEach(state.status,function(status) {
				if ($location.path()===status.link) {
					$scope.index=i;
					$scope.updateButtonVisibility();
				}
				i++;
			});
		});
	});
	$scope.index =0;
	$scope.size = 0;
	$scope.goto = function(link) {
		var i =0;
		angular.forEach($rootScope.states,function (state) {
			angular.forEach(state.status,function(status) {
				if (link===status.link) {
					$scope.index=i;
					$scope.updateButtonVisibility();
					if (status.competence_id) {
						competence_id = status.competence_id;
						competence_field_id = null;
					} else if(status.competence_field_id) {
						$scope.markAsRead(status);
						competence_field_id = status.competence_field_id;
						competence_id = null;
					} else {
						$scope.markAsRead(status);
					}
				}
				i++;
			});
		});
		$location.path(link);
	};
	$scope.markAsRead = function(status) {
		status.value=2;
		DevelopmentPlanService.markLinkAsRead(developmentplan_user_id,status.link);
	}
	$scope.gotoIndex = function(index) {
		var i =0;
		angular.forEach($rootScope.states,function (state) {
			angular.forEach(state.status,function(status) {
				if (i===index) {
					if (status.competence_id) {
						competence_id = status.competence_id;
						competence_field_id = null;
					} else if(status.competence_field_id) {					
						$scope.markAsRead(status);
						competence_field_id = status.competence_field_id;
						competence_id = null;
					} else {
						$scope.markAsRead(status);
					}
					$location.path(status.link);
				}
				i++;
			});
		});
	}
	$scope.isActive = function(link) {
		return $location.path()===link;
	};
	$scope.forward = function() {
		$scope.index++;
		$scope.gotoIndex($scope.index);
		$scope.updateButtonVisibility();
		jq('html,body').scrollTop(0);
	};

	$scope.rewind = function() {
		$scope.index--;
		$scope.gotoIndex($scope.index);
		$scope.updateButtonVisibility();
		jq('html,body').scrollTop(0);
	};
	$scope.updateButtonVisibility = function() {
		$scope.first = $scope.index == 0;
		$scope.last = $scope.index == $scope.size - 1;
	};
}]);