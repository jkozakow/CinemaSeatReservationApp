app = angular.module 'appcinema.api', ['ngResource']

app.factory 'Movie', ['$resource', ($resource) ->
    $resource '/api/movies/:id', id: '@id'
]
