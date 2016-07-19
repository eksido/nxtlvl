controllers.controller('employeeController', [
    '$scope',
    '$timeout',
    'EmployeeService',
    function ($scope, $timeout, EmployeeService) {
        $scope.employees = [];
        $scope.trans = trans;
        $scope.current_user_id = current_user_id;
        $scope.company_id = company_id;
        flatten = function (employees, list, depth) {
            for (var i = 0, l = employees.length; i < l; i++) {
                employees[i].depth = depth;
                list.push(employees[i]);
                flatten(employees[i].employees, list, depth + 1);
            }
        }
        EmployeeService.getEmployeesFuture($scope.company_id).then(function (response) {
            flatten(response.data, $scope.employees, 0);

        });
        $scope.range = function (min, max, step) {
            step = (step == undefined) ? 1 : step;
            var input = [];
            for (var i = min; i <= max; i += step) input.push(i);
            return input;
        };
    }]);