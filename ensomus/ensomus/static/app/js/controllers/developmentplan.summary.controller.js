controllers.controller('developmentPlanSummaryController', [
    '$scope',
    '$rootScope',
    '$timeout',
    '$location',
    'DevelopmentPlanService',
    function ($scope, $rootScope, $timeout, $location, DevelopmentPlanService) {
        $scope.plan = [];
        DevelopmentPlanService.getDevelopmentPlanFuture(developmentplan_user_id).then(function (response) {
            $scope.plan = response.data;
        });
    }]);