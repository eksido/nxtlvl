controllers.controller('developmentPlanEndController', [
	'$scope', 
	'$rootScope',
	'$timeout',
	'$location',
	'DevelopmentPlanService', 
	function ($scope, $rootScope, $timeout,$location,DevelopmentPlanService) {
	$scope.data = {is_private : 'true'};
	$scope.locked = locked;
	$scope.lockdisabled = false;
	$scope.finish = function () {
		$scope.lockdisabled = true;
		DevelopmentPlanService.finishDevelopmentPlanFuture(developmentplan_user_id,$scope.data.is_private=='true').then(function (response) {
			window.location = response.data.redirectUrl;
		});
	}
}]);