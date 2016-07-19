services.service('EmployeeService', ['$http', '$cookies', '$rootScope', function ($http, $cookies, $rootScope) {
    function getEmployeesFuture(company_id) {
        return $http.get('/employee/json/' + company_id);
    };
    return {
        getEmployeesFuture: getEmployeesFuture
    };
}]);