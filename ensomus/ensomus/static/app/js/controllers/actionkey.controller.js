controllers.controller('actionKeyController', ['$scope', '$timeout', 'ActionKeyService', function ($scope, $timeout, ActionKeyService) {

    $scope.init = function (actionKeyToDevelopmentPlanRelationId, isLocked) {
        $scope.actionKeyToDevelopmentPlanRelationId = actionKeyToDevelopmentPlanRelationId;
        $scope.isLocked = isLocked;
        ActionKeyService.getAll(actionKeyToDevelopmentPlanRelationId).then(function (response) {
            $scope.actions = response.data;
        });
    };

    $scope.answerKeyUp = function (event, action) {
        action.changed = action.new_text != action.text;
        if (action.changed) {
            if (action.autoSavePromise) {
                $timeout.cancel(action.autoSavePromise);
            }
            action.autoSavePromise = $timeout(function save() {
                ActionKeyService.saveAction($scope.actionKeyToDevelopmentPlanRelationId, action);
            }, 1000);
        }
    };

    $scope.lock = function () {
        ActionKeyService.lock($scope.actionKeyToDevelopmentPlanRelationId).then(function () {
            $scope.isLocked = true;
        });
    };

    $scope.unLock = function () {
        ActionKeyService.unLock($scope.actionKeyToDevelopmentPlanRelationId).then(function () {
            $scope.isLocked = false;
        });
    };

    $scope.saveActions = function () {
        ActionKeyService.saveActions($scope.actionKeyToDevelopmentPlanRelationId, $scope.actions);
    };
}]);
