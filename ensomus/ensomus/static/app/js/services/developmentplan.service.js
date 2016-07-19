services.service('DevelopmentPlanService', ['$http', '$cookies', '$rootScope', function ($http, $cookies, $rootScope) {
    function getStatesFuture(developmentplan_user_id) {
        return $http.get('/developmentplan/get-states/' + developmentplan_user_id);
    };
    function getCompetenceFuture(competence_id, developmentplan_user_id) {
        return $http.get('/developmentplan/get-competence/' + developmentplan_user_id + '/' + competence_id);
    }

    function getCompetenceFieldFuture(competence_field_id, developmentplan_user_id) {
        return $http.get('/developmentplan/get-competence-field/' + developmentplan_user_id + '/' + competence_field_id);
    }

    function getDevelopmentPlanFuture(developmentplan_user_id) {
        return $http.get('/developmentplan/get/' + developmentplan_user_id);
    }

    function markLinkAsRead(developmentplan_user_id, link) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        var url = '/developmentplan/mark-link-as-read/';
        return $http.post(url, {development_plan_user_id: developmentplan_user_id, link: link});
    }

    function saveQuestion(developmentPlanUserId, question) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        var url = '/developmentplan/save/' + developmentPlanUserId + '/' + question.pk;
        return $http.post(url, {
            response: question.response,
            timestamp: new Date().getTime()
        });
    };
    function finishDevelopmentPlanFuture(developmentplan_user_id, is_private) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        var url = '/developmentplan/finish/';
        return $http.post(url, {
            development_plan_user_id: developmentplan_user_id,
            is_private: is_private
        });
    }

    return {
        getDevelopmentPlanFuture: getDevelopmentPlanFuture,
        getStatesFuture: getStatesFuture,
        getCompetenceFuture: getCompetenceFuture,
        getCompetenceFieldFuture: getCompetenceFieldFuture,
        saveQuestion: saveQuestion,
        finishDevelopmentPlanFuture: finishDevelopmentPlanFuture,
        markLinkAsRead: markLinkAsRead
    };
}]);