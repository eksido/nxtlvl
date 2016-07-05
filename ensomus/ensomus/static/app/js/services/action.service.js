services.service( 'ActionService', [ '$http', '$cookies', '$rootScope', function($http, $cookies, $rootScope) {
	function getAll(developmentPlanId) {
        return $http.get('/action/getall/'+developmentPlanId)
            then(function(actionKeys) {
                return actionKeys;
            });
    };
    function addActionKey(developmentPlanId) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        var url = '/action/add/' + developmentPlanId + '/';
        return $http.post(url).then(function(response) {
            return response;
        });
    };
    return {
        getAll: getAll,
        addActionKey: addActionKey,
    };
}]);