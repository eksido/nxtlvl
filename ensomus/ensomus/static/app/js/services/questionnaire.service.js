services.service('QuestionnaireService', ['$http', '$cookies', '$rootScope', function ($http, $cookies, $rootScope) {
    function get(questionnaireUserId) {
        return $http.get('/questionnaire/get/' + questionnaireUserId)
        then(function (questionnaire) {
            return questionnaire;
        });
    };
    function saveQuestion(questionnaireUserId, question) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        var url = '/questionnaire/save/' + questionnaireUserId + '/' + question.id + '/';
        $http.post(url, 'response=' + question.new_response).then(function (response) {
            question.response = question.new_response;
        });
    };
    function saveQuestions(questionnaireUserId, questions) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        var url = '/questionnaire/saveall/' + questionnaireUserId + '/';
        var responses = [];
        angular.forEach(questions, function (question, key) {
            var response = {
                id: question.id,
                response: question.new_response
            };
            responses.push(response);
        });
        $http.post(url, 'questions=' + JSON.stringify(responses)).then(function (res) {
            angular.forEach(questions, function (question, key) {
                question.response = question.new_response;
            });
            endQuestionnaire(questionnaireUserId);
        });
    };
    function endQuestionnaire(questionnaireUserId) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        var url = '/questionnaire/done/' + questionnaireUserId + '/';
        $http.post(url).then(function (response) {
            window.location = response.data.redirectUrl;
        });
    };
    function toggleIsPrivate(questionnaireUserId) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        return $http.post('/questionnaire/toggleisprivate/' + questionnaireUserId + '/')
        then(function (response) {
            return response;
        });
    };
    return {
        get: get,
        saveQuestion: saveQuestion,
        saveQuestions: saveQuestions,
        toggleIsPrivate: toggleIsPrivate
    };
}]);