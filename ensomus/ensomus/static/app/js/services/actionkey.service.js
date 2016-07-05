services.service( 'ActionKeyService', [ '$http', '$cookies', '$rootScope', function($http, $cookies, $rootScope) {
	function getAll(actionKeyToDevelopmentPlanRelationId) {
        return $http.get('/action/answer/'+actionKeyToDevelopmentPlanRelationId)
            then(function(response) {
                return response;
            });
    };
    function saveAction(actionKeyToDevelopmentPlanRelationId, action) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        var url = '/action/save/' + actionKeyToDevelopmentPlanRelationId + '/' + action.pk + '/';
        $http.post(url, 'text='+action.new_text).then(function(response) {
            action.text = action.new_text;
        });
    };
    function saveActions(actionKeyToDevelopmentPlanRelationId, actions) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        var url = '/action/saveall/' + actionKeyToDevelopmentPlanRelationId + '/';
        var items = [];
        angular.forEach(actions, function(action, key) {
            var item = {
                pk: action.pk,
                text: action.new_text
            };
            items.push(item);
        });
        $http.post(url, 'actions='+JSON.stringify(items)).then(function(res) {
            angular.forEach(actions, function(action, key) {
                action.text = action.new_text;
            });
        });
    };
    function lock(actionKeyToDevelopmentPlanRelationId) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        return $http.post('/action/lock/' + actionKeyToDevelopmentPlanRelationId + '/').then(function(response) {

        });
    };
    function unLock(actionKeyToDevelopmentPlanRelationId) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        return $http.post('/action/unlock/' + actionKeyToDevelopmentPlanRelationId + '/').then(function(response) {
            
        });
    };
    return {
        getAll: getAll,
        lock: lock,
        unLock: unLock,
        saveAction: saveAction,
        saveActions: saveActions
    };
}]);