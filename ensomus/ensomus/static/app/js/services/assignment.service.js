services.service( 'AssignmentService', [ '$http', '$cookies', '$rootScope', function($http, $cookies, $rootScope) {
	function get(assignmentKeyToUserRelationId) {
        return $http.get('/assignment/get/'+assignmentKeyToUserRelationId)
            then(function(assignmentResponses) {
                return assignmentResponses;
            });
    };
    function saveAssignmentResponse(assignmentKeyToUserRelationId, assignmentResponse) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        var url = '/assignment/save/' + assignmentKeyToUserRelationId + '/' + assignmentResponse.pk + '/';
        $http.post(url, 'text_assignment='+assignmentResponse.new_text_assignment+'&'+'text_competence='+assignmentResponse.new_text_competence).then(function(response) {
            assignmentResponse.text_assignment = assignmentResponse.new_text_assignment;
            assignmentResponse.text_competence = assignmentResponse.new_text_competence;
        });
    };
    function saveAssignmentResponses(assignmentKeyToUserRelationId, assignmentResponses) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        var url = '/assignment/saveall/' + assignmentKeyToUserRelationId + '/';
        var assignments = [];
        angular.forEach(assignmentResponses, function(assignmentResponse, key) {
            var assignment = {
                id: assignmentResponse.pk,
                text_assignment: assignmentResponse.new_text_assignment,
                text_competence: assignmentResponse.new_text_competence
            };
            assignments.push(assignment);
        });
        $http.post(url, 'assignments='+JSON.stringify(assignments)).then(function(response) {
            angular.forEach(assignmentResponses, function(assignmentResponse, key) {
                assignmentResponse.text_assignment = assignmentResponse.new_text_assignment;
                assignmentResponse.text_competence = assignmentResponse.new_text_competence;
            });
            window.location = response.data.redirectUrl;
        });
    };
    function toogleIsPrivate(assignmentKeyToUserRelationId) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        return $http.post('/assignment/toggleisprivate/'+assignmentKeyToUserRelationId+'/')
            then(function(response) {
                return response;
            });
    };
    return {
        get: get,
        saveAssignmentResponse: saveAssignmentResponse,
        saveAssignmentResponses: saveAssignmentResponses,
        toogleIsPrivate: toogleIsPrivate
    };
}]);