var app = angular.module('app', ['ui.bootstrap']);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.service("svc", function ($http) {
    this.svc_ListData = function (PageIndex, PageSize, SearchBy, Keywords) {
        var params = { 
            PageIndex: PageIndex,
            PageSize: PageSize,
            SearchBy: SearchBy,
            Keywords: Keywords,
        }
        var response = $http({
            method: "post",
            url: "/Bahan/ListData",
            data: JSON.stringify(params),
            datatype: "json"
        });
        return response;
    }
});

app.controller('ctrl', function ($scope, $timeout, svc, common) {

    $scope.data = [];
    $scope.PageIndex = 1;
    $scope.PageSize = 5;
    $scope.SearchBy = '';
    $scope.Keywords = '';
    $scope.TotalRecords = 0;
    $scope.Options = {};
    $scope.Options.SearchBy = [
        {id: '', name:'All'},
        {id: 'A.bahan_code', name:'Bahan Code'},
        {id: 'A.bahan_name', name:'Bahan Name'},
    ];
    $scope.Options.PageSize = [5, 10, 25, 50, 100];

    $scope.Paging = function () {
        var PageIndex = $scope.PageIndex;
        var PageSize = $scope.PageSize;
        var SearchBy = $scope.SearchBy;
        var Keywords = $scope.Keywords;

        var proc = svc.svc_ListData(PageIndex, PageSize, SearchBy, Keywords);
        proc.then(function (response) {
            var data = response.data;
            console.log(data);
            if (data.ProcessSuccess) {
                $scope.Data = data.d.List;
                $scope.TotalRecords = data.d.TotalRecords;
            } else {
                $scope.Data = [];
                $scope.TotalRecords = 0;
                console.log(data.InfoMessage);
            }
        }, 
            function (data, status) {
            alert('Error in Save Update ' + status);
        });
    }

    $scope.Paging();

    $scope.AddNew = function () {
        location.href = 'Entry'
    };
    $scope.Edit = function (uid) {
        location.href = 'Entry?uid=' + uid;
    };
});