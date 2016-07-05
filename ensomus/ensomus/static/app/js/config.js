nxtlvl.config([
  '$interpolateProvider',
  '$routeProvider',
  'urls',
  '$sceDelegateProvider',
  '$compileProvider',
  function($interpolateProvider,$routeProvider,urls,$sceDelegateProvider,$compileProvider) {
  //$interpolateProvider.startSymbol('{[{');
  //$interpolateProvider.endSymbol('}]}');
  $sceDelegateProvider.resourceUrlWhitelist([
      'self',
      'http://static.nxtlvl.webfactional.com/**',
      'http://static.nxtlvl.dk/**'
    ]);
  $routeProvider
  .when('/',{
  	templateUrl: urls.intro,
  })
  .when('/intro-competence',{
    templateUrl: urls.competenceintro,
    controller: 'developmentPlanCompetenceIntroController'
  })
  .when('/summary',{
    templateUrl: urls.summary,
    controller: 'developmentPlanSummaryController'
  })
  .when('/end',{
    templateUrl: urls.end,
    controller: 'developmentPlanEndController'
  })
  .otherwise({
  	templateUrl: urls.competence,
  	controller: 'developmentPlanCompetenceController'
  });
}]);