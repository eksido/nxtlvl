controllers.controller('developmentPlanCompetenceController', [
    '$scope',
    '$rootScope',
    '$timeout',
    '$location',
    'DevelopmentPlanService',
    function ($scope, $rootScope, $timeout, $location, DevelopmentPlanService) {
        $scope.competence_id = competence_id;
        $scope.locked = locked;
        if (competence_id) {
            DevelopmentPlanService.getCompetenceFuture(competence_id, developmentplan_user_id).then(function (response) {
                $scope.competence = response.data;
                $scope.competence_field = null;
            });
        } else if (competence_field_id) {
            DevelopmentPlanService.getCompetenceFieldFuture(competence_field_id, developmentplan_user_id).then(function (response) {
                $scope.competence_field = response.data;
                $scope.competence = null;
            });
        } else {
            $location.path("/");
        }
        $scope.change = function (question) {
            alert(question.pk);
        }
        $scope.answerChange = function (event, question) {
            question.changed = question.response != question.new_response;
            if (question.changed) {
                if (question.autoSavePromise) {
                    $timeout.cancel(question.autoSavePromise);
                }
                var cid = competence_id;
                question.autoSavePromise = $timeout(function save() {
                    DevelopmentPlanService.saveQuestion(developmentplan_user_id, question).then(function (response) {
                        console.log(response);
                        angular.forEach($rootScope.states, function (state) {
                            angular.forEach(state.status, function (status) {
                                if (status.competence_id === cid) {
                                    var amount = 0;
                                    var count = $scope.competence.questions.length;
                                    for (var i = 0; i < count; i++) {
                                        if ($scope.competence.questions[i].response) {
                                            amount++;
                                        }
                                    }
                                    if (count == amount) {
                                        status.value = 2;
                                    } else if (amount == 0) {
                                        status.value = 0;
                                    } else {
                                        status.value = 1;
                                    }
                                }
                            });
                        });
                    });
                }, 1000);
            }
        };
    }]);