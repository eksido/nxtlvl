controllers.controller('actionController', ['$scope', '$timeout', 'ActionService', function ($scope, $timeout, ActionService) {
    $scope.actionKeys = [];

    $scope.init = function (developmentPlanId) {
        $scope.developmentPlanId = developmentPlanId;
        ActionService.getAll(developmentPlanId).then(function (response) {
            $scope.actionKeys = response.data;
        });
    };

    $scope.addActionKey = function () {
        ActionService.addActionKey($scope.developmentPlanId).then(function (response) {
            $scope.actionKeys.splice(0, 0, response.data);
        });
    };

    $scope.answerKeyUp = function (event, assignmentResponse) {
        assignmentResponse.changed = assignmentResponse.text_assignment != assignmentResponse.new_text_assignment || assignmentResponse.text_competence != assignmentResponse.new_text_competence;
        if (assignmentResponse.changed) {
            if (assignmentResponse.autoSavePromise) {
                $timeout.cancel(assignmentResponse.autoSavePromise);
            }
            assignmentResponse.autoSavePromise = $timeout(function save() {
                AssignmentService.saveAssignmentResponse($scope.assignmentKeyToUserRelationId, assignmentResponse);
            }, 1000);
        }
    };
}]);
