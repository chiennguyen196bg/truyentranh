app.controller('randomController', function($scope, $http) { 
	$http.get("/json/random")
    .then(function(response) {
        $scope.itemRandom = response.data;
        if ($scope.itemRandom.summary == ""){
        	$scope.itemRandom.summary = "Truyện tranh 
        	<strong>"+$scope.itemRandom.name+"</strong>
        	 nội dung đang được cập nhật. 
        	 Ghé thăm Truyen47.com để được đọc các chương mới nhất của 
        	 <strong>"+$scope.itemRandom.name+"</strong>"
        }
        // $scope.statuscode = response.status;
       	// $scope.statustext = response.statustext;
    });

});