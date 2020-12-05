var app = angular.module('app', []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.service("svc", function ($http) {
    this.svc_SaveUpdate = function (header, detail) {
        var params = { 
            header: header,
            detail: detail
        }
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
    // region declare
    $scope.Uid = GetQueryString()['uid'];

    $scope.header = { item_type: '' };

    $scope.detail = [];
    $scope.deletedDetail = [];

    $scope.bahan_uid = '';
    $scope.bahan_code = '';
    $scope.bahan_name = '';
    $scope.recipe_qty = 0;
    $scope.unit_code = '';

    $scope.Options = {};
    $scope.Options.ItemType = [
        {id: '', name: 'Please select one.'},
        {id: 'Makanan', name: 'Makanan'},
        {id: 'Minuman', name: 'Minuman'},
    ];

    $scope.PopupSelect = {
        Bahan: function (i) {
            console.log(i);
            $scope.bahan_uid = i.uid;
            $scope.bahan_code = i.bahan_code;
            $scope.bahan_name = i.bahan_name;
        },
    };
    // end region declare

    // region get options
    common.GetOptions('mst_unit', 'unit_code', 'unit_name').then(function (response) {
        var data = response.data;
        if (data.ProcessSuccess) {
            $scope.Options.Unit = data.List;
        } else {
            console.log(data.InfoMessage);
        }
    }, 
        function (data, status) {
        alert('Error in Get Options ' + status);
    });
    // end region get options

    // region get data
    $scope.GetData = function () {
        var uid = $scope.Uid;
        if (uid){
            var proc = svc.svc_GetData(uid);
            proc.then(function (response) {
                var data = response.data;
                if (data.ProcessSuccess) {
                    $scope.header = data.d;
                    $scope.detail = data.d.recipeDetailList;
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
    // end region get data

    // region detail
    $scope.AddRecipe = function () {
        $scope.detail.push({
            bahan_uid: $scope.bahan_uid,
            bahan_code: $scope.bahan_code,
            bahan_name: $scope.bahan_name,
            qty: $scope.recipe_qty,
            unit_code: $scope.unit_code
        });
    };
    $scope.RemoveRecipe = function (d, index) {
        $scope.deletedDetail.push(d);
        $scope.detail.splice(index, 1);
    };
    $scope.ResetRecipeForm = function () {
        $scope.bahan_uid = '';
        $scope.bahan_code = '';
        $scope.bahan_name = '';
        $scope.recipe_qty = 0;
        $scope.unit_code = '';
    };
    // end region detail

    $scope.SaveUpdate = function () {
        // prepare header
        var header = {
            uid: $scope.Uid,
            item_code: $scope.header.item_code,
            item_name: $scope.header.item_name,
            price: $scope.header.price,
            item_type: $scope.header.item_type,
            rowstatus: 1
        };

        // prepare detail
        var detail = [];
        for (d of $scope.detail) {
            detail.push({
                uid: d.uid,
                item_uid: d.item_uid,
                item_code: d.item_code,
                item_name: d.item_name,
                bahan_uid: d.bahan_uid,
                bahan_code: d.bahan_code,
                bahan_name: d.bahan_name,
                qty: d.qty,
                unit_code: d.unit_code,
                rowstatus: 1
            });
        }
        for (d of $scope.deletedDetail) {
            if (d.uid) {
                detail.push({
                    uid: d.uid,
                    item_uid: d.item_uid,
                    item_code: d.item_code,
                    item_name: d.item_name,
                    bahan_uid: d.bahan_uid,
                    bahan_code: d.bahan_code,
                    bahan_name: d.bahan_name,
                    qty: d.qty,
                    unit_code: d.unit_code,
                    rowstatus: 0
                });
            }
        }

        var proc = svc.svc_SaveUpdate(header, detail);
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
        // prepare header
        var header = {
            uid: $scope.Uid,
            item_code: $scope.header.item_code,
            item_name: $scope.header.item_name,
            price: $scope.header.price,
            item_type: $scope.header.item_type,
            rowstatus: 0
        };

        // prepare detail
        var detail = [];
        for (d of $scope.detail) {
            detail.push({
                uid: d.uid,
                item_uid: d.item_uid,
                item_code: d.item_code,
                item_name: d.item_name,
                bahan_uid: d.bahan_uid,
                bahan_code: d.bahan_code,
                bahan_name: d.bahan_name,
                qty: d.qty,
                unit_code: d.unit_code,
                rowstatus: 1
            });
        }
        for (d of $scope.deletedDetail) {
            if (d.uid) {
                detail.push({
                    uid: d.uid,
                    item_uid: d.item_uid,
                    item_code: d.item_code,
                    item_name: d.item_name,
                    bahan_uid: d.bahan_uid,
                    bahan_code: d.bahan_code,
                    bahan_name: d.bahan_name,
                    qty: d.qty,
                    unit_code: d.unit_code,
                    rowstatus: 0
                });
            }
        }

        var proc = svc.svc_SaveUpdate(header, detail);
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