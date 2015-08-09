var app = angular.module('LockrWebApp', ['vxWamp']);

app.config(['$wampProvider', function($wampProvider) {
  $wampProvider.init({
    url: 'ws://localhost:8080/ws',
    realm: 'lockr'
  });
}]);

app.controller('MainCtrl', ['$scope', '$wamp', function($scope, $wamp) {

  var uuid;

  $scope.seat_state = false;
  $scope.btn_msg = "Wait for it...";
  $scope.btn_disabled = true;

  function handleError(err) {
    $scope.error = err;
    $scope.btn_disabled = true;
    $scope.seat_state = false;
    $scope.btn_msg = "Shit happened :/";
  }

  $wamp.subscribe('lockr.seat.unlocked', function(locker_id) {
    $scope.btn_msg = "Lock the seat";
    $scope.seat_state = true;
    $scope.btn_disabled = false;
  });

  $wamp.subscribe('lockr.seat.locked', function(locker_id) {
    $scope.seat_state = false;
    if (locker_id == uuid) {
      $scope.btn_msg = "Release the seat";
    } else {
      $scope.btn_msg = "The seat is locked by someone else";
      $scope.btn_disabled = true;
    }
  });

  $wamp.call('lockr.seat.get_id').then(
    function(res) {
      uuid = res;
    }, handleError
  );

  $wamp.publish('lockr.seat.refresh');
    
  $scope.toggleLock = function() {
    if ($scope.seat_state) {
      $wamp.call('lockr.seat.lock', [uuid]).then(
        function(res) {
          if (res) {
            $scope.seat_state = false;
          }
        }, handleError);
    } else {
      $wamp.call('lockr.seat.unlock', [uuid]).then(
        function(res) {
          if (res) {
            $scope.seat_state = true;
          }
        }, handleError);
    }
  };
}]);

app.run(['$wamp', function($wamp) {
  $wamp.open();
}]);
