angular
    .module('app')
    .service('bahanPopupSvc', ['$http', function ($http) {
        var self = this;
        self.svc_BahanListData = function (PageIndex, PageSize, SearchBy, Keywords) {
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
        };
    }])
    .component('bahanPopup', {
        templateUrl: `/static/japps/itemjs/component/bahan-popup/bahan-popup-template.html?${new Date().getTime()}`,
        bindings: {
            id: '@popupId',
            Select: '<onSelect',
        },
        controller: function ($scope, bahanPopupSvc, common) {
            var $ctrl = this;
            $ctrl.$onInit = function () {
                $ctrl.SearchBy = '';
                $ctrl.Keywords = '';
                $ctrl.Data = [];
                $ctrl.PageIndex = 1;
                $ctrl.PageSize = 10;
                $ctrl.TotalRecords = 0;
                $ctrl.Options = {};

                $ctrl.Options.SearchBy = [
                    { id: '', name: 'All' },
                    { id: 'A.bahan_code', name: 'Bahan Code' },
                    { id: 'A.bahan_name', name: 'Bahan Name' },
                ];

                $ctrl.Paging = function () {
                    var PageIndex = $ctrl.PageIndex;
                    var PageSize = $ctrl.PageSize;
                    var SearchBy = $ctrl.SearchBy;
                    var Keywords = $ctrl.Keywords;

                    bahanPopupSvc.svc_BahanListData(PageIndex, PageSize, SearchBy, Keywords).then(function (response) {
                        var data = response.data;
                        console.log(data);
                        if (data.ProcessSuccess) {
                            $ctrl.Data = data.d.List;
                            $ctrl.TotalRecords = data.d.TotalRecords;
                        } else {
                            $ctrl.Data = [];
                            $ctrl.TotalRecords = 0;
                            console.log(data.InfoMessage);
                        }
                    }, function (data, status) {
                        alert(status);
                    });
                };

                $ctrl.closePopup = function () {
                    $(`#${$ctrl.id}`).modal('hide');
                    // $('body').removeClass('modal-open');
                    // $('.modal-backdrop').remove();
                };

                $scope.$on($ctrl.id, function () {
                    $ctrl.SearchBy = '';
                    $ctrl.Keywords = '';
                    $ctrl.Data = [];
                    $ctrl.PageIndex = 1;
                    $ctrl.Paging();
                });
            };
        }
    });