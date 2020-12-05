angular.module('app')
    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])
    .service('common', ['$http', function ($http) {
        var self = this;
        
        self.GetOptions = function (table_name, id_field, name_field) {
            var params = { 
                table_name: table_name,
                id_field: id_field,
                name_field: name_field
            }
            var response = $http({
                method: "post",
                url: "/Common/GetOptions",
                data: JSON.stringify(params),
                datatype: "json"
            });
            return response;
        }

        self.convDate = function (str) {
            var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Agu', 'Sep', 'Oct', 'Nov', 'Dec'];
            var date = new Date(str),
              mnth = months[date.getMonth()],
              day = ("0" + date.getDate()).slice(-2);
            return [day, mnth, date.getFullYear()].join(" ");
        };

        
    }])
    .directive('expand', function () {
        function link(scope, element, attrs) {
            scope.$on('onExpandAll', function (event, args) {
                scope.expanded = args.expanded;
            });
        }
        return {
            link: link
        };
    })
    .directive('showData', function ($compile) {
        return {
            scope: true,
            link: function (scope, element, attrs) {
                var el;

                attrs.$observe('template', function (tpl) {
                    if (angular.isDefined(tpl)) {
                        // compile the provided template against the current scope
                        el = $compile(tpl)(scope);

                        // stupid way of emptying the element
                        element.html("");

                        // add the template content
                        element.append(el);
                    }
                });
            }
        };
    })
    .directive('isolateForm', function () {
        return {
            restrict: 'A',
            require: '?form',
            link: function (scope, element, attrs, formController) {
                if (!formController) {
                    return;
                }

                var parentForm = formController.$$parentForm; // Note this uses private API
                if (!parentForm) {
                    return;
                }

                // Remove this form from parent controller
                parentForm.$removeControl(formController);
            }
        };
    })
    .directive('button', function () {
        return {
            restrict: 'E',
            link: function (scope, elem, attrs) {
                if (attrs.ngClick || attrs.href === '' || attrs.href === '#') {
                    elem.on('click', function (e) {
                        e.preventDefault();
                    });
                }
            }
        };
    })
    .directive('loading', ['$http', function ($http) {
        return {
            restrict: 'A',
            link: function (scope, elm, attrs) {
                scope.isLoading = function () {
                    return $http.pendingRequests.length > 0;
                };

                scope.$watch(scope.isLoading, function (v) {
                    if (v) {
                        elm.show();
                    } else {
                        elm.hide();
                    }
                });
            }
        };
    }])
    .directive('thousandSeparator', function () {
        return {
            restrict: "A",
            require: 'ngModel',
            link: function (scope, elem, attrs, ngModelCtrl) {

                elem.bind('blur', function (e) {
                    if (attrs.minSize && elem[0].value != 0) {
                        var amount = elem[0].value.replace(/[A-Za-z\,]/g, '');
                        if ((elem[0].value != '') && (!amount.match(/^$/))) {
                            elem[0].value = parseFloat(amount).toFixed(attrs.minSize);
                            setDisplayNumber(elem[0].value);
                        }
                    }
                });
                scope.$watch(scope.isLoading, function (v) {
                    if (!v) {
                        if (attrs.minSize && elem[0].value != 0) {
                            var amount = elem[0].value.replace(/[A-Za-z\,]/g, '');
                            if ((elem[0].value != '') && (!amount.match(/^$/))) {
                                elem[0].value = parseFloat(amount).toFixed(attrs.minSize);
                                setDisplayNumber(elem[0].value);
                            }
                        }
                    }
                });

                ngModelCtrl.$formatters.push(function (modelValue) {
                    var value = setModelNumber(modelValue);
                    var maxValid = true;
                    var minValid = true;
                    var nonZeroValid = true;
                    if (attrs.max) {
                        maxValid = value <= attrs.max;
                        ngModelCtrl.$setValidity('max', maxValid);
                    }
                    if (attrs.min) {
                        minValid = value >= attrs.min;
                        ngModelCtrl.$setValidity('min', minValid);
                    }
                    if (attrs.nonZero != undefined) {
                        nonZeroValid = value != 0;
                        ngModelCtrl.$setValidity('nonZero', nonZeroValid);
                    }

                    return setDisplayNumber(modelValue, true);
                });
                ngModelCtrl.$parsers.push(function (viewValue) {
                    setDisplayNumber(viewValue);

                    var value = setModelNumber(viewValue);
                    var maxValid = true;
                    var minValid = true;
                    var nonZeroValid = true;
                    if (attrs.max) {
                        maxValid = value <= attrs.max;
                        ngModelCtrl.$setValidity('max', maxValid);
                    }
                    if (attrs.min) {
                        minValid = value >= attrs.min;
                        ngModelCtrl.$setValidity('min', minValid);
                    }
                    if (attrs.nonZero != undefined) {
                        nonZeroValid = value != 0;
                        ngModelCtrl.$setValidity('nonZero', nonZeroValid);
                    }

                    return maxValid && minValid && nonZeroValid ? value : undefined;
                });

                function setDisplayNumber(val, formatter) {
                    val = val || '0';

                    var valStr, displayValue;

                    valStr = val.toString();
                    displayValue = valStr.replace(/[A-Za-z\,]/g, '');
                    displayValue = attrs.integer != undefined ? parseInt(displayValue) : parseFloat(displayValue);

                    // handle leading character -/0
                    if (valStr === '-' || valStr === '0-') {
                        displayValue = '-';
                    }

                        //handle decimal
                    else {
                        var decimalLength = valStr.substr(valStr.indexOf('.') + 1).length;
                        displayValue = displayValue || displayValue === 0 ? displayValue.toLocaleString(undefined, {
                            minimumFractionDigits: attrs.integer != undefined || valStr.indexOf('.') === -1 || decimalLength > 4 ? 0 : decimalLength,
                            maximumFractionDigits: attrs.integer != undefined ? 0 : 4
                        }) : '0';
                    }

                    // handle dot
                    if (attrs.integer === undefined && displayValue.indexOf('.') === -1 && valStr.slice(-1) === '.') {
                        displayValue += '.';
                    }

                    if (typeof formatter !== 'undefined') {
                        return displayValue ? displayValue : 0;
                    } else {
                        elem.val(displayValue);
                    }
                }

                function setModelNumber(val) {
                    val = val || '0';

                    var modelNum = val.toString().replace(/[A-Za-z\,]/g, '');
                    modelNum = attrs.integer != undefined ? parseInt(modelNum) : +(Math.round(parseFloat(modelNum) + "e+4") + "e-4");

                    return modelNum ? modelNum : 0;
                }
            }
        };
    })
    .directive('isValid', function () {
        //https://stackoverflow.com/questions/26547488/angularjs-how-to-set-validity-based-on-custom-boolean-value
        return {
            scope: {
                isValid: '='
            },
            require: 'ngModel',
            link: function (scope, elm, attrs, ngModel) {

                scope.$watch('isValid', function (value) {
                    ngModel.$setValidity('isValid', !!value);
                });

            }
        };
    })
    .directive('onEnterFunction', function () {
        return function (scope, element, attrs) {
            element.bind("keydown keypress", function (event) {
                if(event.which === 13) {
                    scope.$apply(function (){
                        scope.$eval(attrs.onEnterFunction);
                    });

                    event.preventDefault();
                }
            });
        };
    })
    .component('datepicker', {
        bindings: {
            name: '@',
            placeholder: '@',
            model: '=ngModel',
            disabled: '=ngDisabled',
            required: '=ngRequired',
            changed: '&ngChange',
            format: '<',
        },
        template:
            '<div class="input-group">' +
                '<input type="text" name="{{$ctrl.name}}" class="form-control form-control-sm" placeholder="{{$ctrl.placeholder}}" uib-datepicker-popup="{{$ctrl.format || \'dd MMMM yyyy\'}}" ng-class="{\'rounded-sm\':$ctrl.disabled}" ng-model="$ctrl.model" is-open="$ctrl.opened" datepicker-options="$ctrl.options" ng-required="$ctrl.required" ng-change="$ctrl.changed()" close-text="Close" readonly />' +
                '<span class ="input-group-append" ng-hide="$ctrl.disabled">' +
                    '<button type="button" class ="btn btn-sm btn-secondary" ng-click="$ctrl.open($event)" ng-disabled="$ctrl.disabled">' +
                    '<i class ="fa-svg-icon">' +
                        '<svg width="1792" height="1792" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg"><path d="M192 1664h288v-288h-288v288zm352 0h320v-288h-320v288zm-352-352h288v-320h-288v320zm352 0h320v-320h-320v320zm-352-384h288v-288h-288v288zm736 736h320v-288h-320v288zm-384-736h320v-288h-320v288zm768 736h288v-288h-288v288zm-384-352h320v-320h-320v320zm-352-864v-288q0-13-9.5-22.5t-22.5-9.5h-64q-13 0-22.5 9.5t-9.5 22.5v288q0 13 9.5 22.5t22.5 9.5h64q13 0 22.5-9.5t9.5-22.5zm736 864h288v-320h-288v320zm-384-384h320v-288h-320v288zm384 0h288v-288h-288v288zm32-480v-288q0-13-9.5-22.5t-22.5-9.5h-64q-13 0-22.5 9.5t-9.5 22.5v288q0 13 9.5 22.5t22.5 9.5h64q13 0 22.5-9.5t9.5-22.5zm384-64v1280q0 52-38 90t-90 38h-1408q-52 0-90-38t-38-90v-1280q0-52 38-90t90-38h128v-96q0-66 47-113t113-47h64q66 0 113 47t47 113v96h384v-96q0-66 47-113t113-47h64q66 0 113 47t47 113v96h128q52 0 90 38t38 90z"/></svg>' +
                    '</i>' +
                    '</button>' +
                '</span>' +
            '</div>',
        controller: function () {
            var $ctrl = this;
            $ctrl.open = function ($event) {
                $ctrl.opened = true;
            };
            $ctrl.options == {
                formatYear: 'yy',
                startingDay: 1,
            };
        }
    })
    .component('datetimepicker', {
        bindings: {
            name: '@',
            placeholder: '@',
            model: '=ngModel',
            disabled: '=ngDisabled',
            required: '=ngRequired',
            changed: '&ngChange',
            format: '<',
        },
        template:
            '<div class="input-group">' +
                '<input type="text" name="{{$ctrl.name}}" class="form-control form-control-sm" placeholder="{{$ctrl.placeholder}}" datetime-picker="dd MMMM yyyy HH:mm" is-open="$ctrl.opened" ng-class="{\'rounded-sm\':$ctrl.disabled}" ng-model="$ctrl.model" ng-required="$ctrl.required" ng-change="$ctrl.changed()" close-text="Close" readonly />' +
                '<span class ="input-group-append" ng-hide="$ctrl.disabled">' +
                    '<button type="button" class ="btn btn-sm btn-secondary" ng-click="$ctrl.open($event)" ng-disabled="$ctrl.disabled">' +
                    '<i class ="fa-svg-icon">' +
                        '<svg width="1792" height="1792" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg"><path d="M192 1664h288v-288h-288v288zm352 0h320v-288h-320v288zm-352-352h288v-320h-288v320zm352 0h320v-320h-320v320zm-352-384h288v-288h-288v288zm736 736h320v-288h-320v288zm-384-736h320v-288h-320v288zm768 736h288v-288h-288v288zm-384-352h320v-320h-320v320zm-352-864v-288q0-13-9.5-22.5t-22.5-9.5h-64q-13 0-22.5 9.5t-9.5 22.5v288q0 13 9.5 22.5t22.5 9.5h64q13 0 22.5-9.5t9.5-22.5zm736 864h288v-320h-288v320zm-384-384h320v-288h-320v288zm384 0h288v-288h-288v288zm32-480v-288q0-13-9.5-22.5t-22.5-9.5h-64q-13 0-22.5 9.5t-9.5 22.5v288q0 13 9.5 22.5t22.5 9.5h64q13 0 22.5-9.5t9.5-22.5zm384-64v1280q0 52-38 90t-90 38h-1408q-52 0-90-38t-38-90v-1280q0-52 38-90t90-38h128v-96q0-66 47-113t113-47h64q66 0 113 47t47 113v96h384v-96q0-66 47-113t113-47h64q66 0 113 47t47 113v96h128q52 0 90 38t38 90z"/></svg>' +
                    '</i>' +
                    '</button>' +
                '</span>' +
            '</div>',
        controller: function () {
            var $ctrl = this;
            $ctrl.open = function ($event) {
                $ctrl.opened = true;
            };
        }
    })
    .filter('sum', function () {
        return function (data, key) {
            if (!data)
                return 0;

            var sum = 0;
            if (key) {
                angular.forEach(data, function (obj, objKey) {
                    let num = parseFloat(obj[key]);
                    sum += num ? num : 0;
                });
            }
            else {
                angular.forEach(data, function (obj) {
                    let num = parseFloat(obj);
                    sum += num ? num : 0;
                });
            }

            return sum;
        };
    })
    .filter('thousandSeparator', function () {
        return function (data, minSize) {
            num = parseFloat(data);
            return num ? num.toLocaleString(undefined, { maximumFractionDigits: 4 }) : data;
        }
    })
    .filter("FormatDate", function () {
        var re = /\/Date\(([0-9]*)\)\//;
        return function (x) {
            var m = x.match(re);
            if (m) return new Date(parseInt(m[1]));
            else return null;
        };
    })
    .filter('split', function () {
        return function (input, splitChar, splitIndex) {
            // do some bounds checking here to ensure it has that index
            return input.split(splitChar)[splitIndex];
        }
    });

function GetQueryString() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

function SetQueryString(q) {
    q = q && (q.startsWith('?') && q || '?' + q) || '';
    window.history.replaceState(null, null, window.location.pathname + q);
}

function NEWID() {
    //https://stackoverflow.com/questions/105034/create-guid-uuid-in-javascript
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}