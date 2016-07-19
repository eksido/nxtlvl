directives.directive('simplehtml', function () {
    return function (scope, element, attr) {
        scope.$watch(attr.simplehtml, function (value) {
            element.html(scope.$eval(attr.simplehtml));
        })
    }
});