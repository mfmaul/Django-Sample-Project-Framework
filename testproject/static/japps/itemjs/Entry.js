var app = angular.module('app', []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.service("svc", function ($http) {
    this.svc_SaveUpdate = function (header) {
        var params = { header: header }
        var response = $http({
            method: "post",
            url: "/Item/ItemSaveUpdate",
            data: JSON.stringify(params),
            datatype: "json"
        });
        return response;
    }
    this.svc_GetData = function (uid) {
        var params = { uid: uid }
        var response = $http({
            method: "post",
            url: "/Item/ItemGetData",
            data: JSON.stringify(params),
            datatype: "json"
        });
        return response;
    }
});

app.controller('ctrl', function ($scope, $timeout, svc, common) {
    $scope.Uid = GetQueryString()['uid'];
    $scope.header = {};

    $scope.GetData = function () {
        var uid = $scope.Uid;
        if (uid){
            var proc = svc.svc_GetData(uid);
            proc.then(function (response) {
                var data = response.data;
                if (data.ProcessSuccess) {
                    $scope.header = data.d.List[0];
                    SetQueryString(`uid=${$scope.Uid}`);
                } else {
                    console.log(data.InfoMessage);
                    SetQueryString();
                }
            }, 
                function (data, status) {
                alert('Error in Save Update ' + status);
            });
        }
        
    }

    $scope.GetData();

    $scope.SaveUpdate = function () {
        var header = {
            uid: $scope.Uid,
            item_code: $scope.header.item_code,
            item_name: $scope.header.item_name,
            price: $scope.header.price,
            rowstatus: 1
        };
        var proc = svc.svc_SaveUpdate(header);
        proc.then(function (response) {
            var data = response.data;
            console.log(data);
            if (data.ProcessSuccess){
                $scope.header = data.d;
                $scope.Uid = $scope.header.uid;
                $scope.GetData();
                alert('Save success.');
            } else {
                alert('Error : ' + data.InfoMessage);
            }
        }, 
            function (data, status) {
            alert('Error in Save Update ' + status);
        });
    }
    
    $scope.Delete = function () {
        var header = {
            uid: $scope.Uid,
            item_code: $scope.header.item_code,
            item_name: $scope.header.item_name,
            price: $scope.header.price,
            rowstatus: 0
        };
        var proc = svc.svc_SaveUpdate(header);
        proc.then(function (response) {
            var data = response.data;
            if (data.ProcessSuccess){
                alert('Data has been deleted.');
                location.href = 'List'
            } else {
                alert('Error : ', data.InfoMessage);
            }
        }, 
            function (data, status) {
            alert('Error in Save Update ' + status);
        });
    }

    $scope.Back = function () {
        location.href = 'List'
    }

});