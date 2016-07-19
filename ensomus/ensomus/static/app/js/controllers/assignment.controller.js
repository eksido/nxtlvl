controllers.controller('assignmentController', ['$scope', '$timeout', 'AssignmentService', function ($scope, $timeout, AssignmentService) {
    $scope.privateText = '';

    $scope.init = function (assignmentKeyToUserRelationId, isPrivate, isMine) {
        $scope.assignmentKeyToUserRelationId = assignmentKeyToUserRelationId;
        AssignmentService.get(assignmentKeyToUserRelationId).then(function (response) {
            $scope.assignmentResponses = response.data;
        });
        $scope.isPrivate = isPrivate;
        $scope.isMine = isMine;
    };

    $scope.toggleIsPrivate = function () {
        AssignmentService.toogleIsPrivate($scope.assignmentKeyToUserRelationId).then(function (response) {
            $scope.isPrivate = !$scope.isPrivate;
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

    $scope.saveAssignmentResponses = function () {
        AssignmentService.saveAssignmentResponses($scope.assignmentKeyToUserRelationId, $scope.assignmentResponses);
    };

    $scope.$watch('isPrivate', function (value) {
        var text = $scope.isMine ? 'leder' : 'medarbejder';
        $scope.privateText = (value ? 'Gør synlig for din ' : 'Skjul for din ') + text;
    });
}]);
