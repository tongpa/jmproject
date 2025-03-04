var app = angular.module("poll", ['ui.bootstrap']);
	
	app.controller("pollController", function($scope, $http) {
		$scope.url = '/ang/getQuestion';
		$scope.content = [];
		
		$scope.fetchContent = function (){
	        $http.get($scope.url).success(function(response) {
	        	$scope.content = response.questions[0].question;;
	        	 
	        	}
	        );
		};
	

	    $scope.fetchContent();
	    
	
	});
	
	app.controller("pagingController",function($scope, $log) {
		$scope.totalItems = 64;
		$scope.currentPage = 4;

		  $scope.setPage = function (pageNo) {
			$scope.currentPage = pageNo;
		  };

	  $scope.pageChanged = function() {
		$log.log('Page changed to: ' + $scope.currentPage);
	  };

	  $scope.maxSize = 5;
	  $scope.bigTotalItems = 175;
	  $scope.bigCurrentPage = 1;
	});
	
	/*
	app.filter('partition', [
	                      'filterStabilize',
	                      function(stabilize) {

	                        function partition(arr, size) {

	                          var newArr = [];

	                          for (var i=0; i<arr.length; i+=size) {
	                            newArr.push(arr.slice(i, i+size));
	                          }

	                          return newArr;

	                        }

	                        return stabilize(partition);

	                      }
	                    ]);
	
	app.factory('filterStabilize', [
	                      'memoize',
	                      function(memoize) {

	                        function service(fn) {

	                          function filter() {
	                            var args = [].slice.call(arguments);
	                            // always pass a copy of the args so that the original input can't be modified
	                            args = angular.copy(args);
	                            // return the `fn` return value or input reference (makes `fn` return optional)
	                            var filtered = fn.apply(this, args) || args[0];
	                            return filtered;
	                          }

	                          var memoized = memoize(filter);

	                          return memoized;

	                        }

	                        return service;

	                      }
	                    ]);
	app.factory('memoize', [
	                      function() {

	                        function service() {
	                          return memoizeFactory.apply(this, arguments);
	                        }

	                        function memoizeFactory(fn) {

	                          var cache = {};

	                          function memoized() {

	                            var args = [].slice.call(arguments);

	                            var key = JSON.stringify(args);

	                            if (cache.hasOwnProperty(key)) {
	                              return cache[key];
	                            }

	                            cache[key] = fn.apply(this, arguments);

	                            return cache[key];

	                          }

	                          return memoized;

	                        }

	                        return service;

	                      }
	                    ]);
	
	*/
	app.directive('contentItemIndex', function ($compile, $templateCache) {
		console.log("contentItemIndex");
		
		
		
		var getTemplate = function(contentType) {
	         var template = '';
	          
	         template ="/template/questionindextpl.html";

	         return template;
	     }
		
		
		var directive = {};
	     directive.restrict = 'E';
	     //directive.link =  linker;	     
	     directive.template =  '<ng-include src="getTemplateUrl()"/>';
	     directive.controller = function($scope) {
	         $scope.getTemplateUrl = function() {  
	        	  
	        	 return getTemplate($scope.content.type);
	           
	         }
	       }
	     directive.scope  =  {
					             content:'=' 
					         }
	     
	     return directive;
	});
	app.directive('contentItem', function ($compile, $templateCache) {
	    /* EDITED FOR BREVITY */

	     console.log("show");
	     
	     var imageTemplate = '<div class="entry-photo"><h2>&nbsp;</h2><div class="entry-img"><span><a href="{{rootDirectory}}{{content.data}}"><img ng-src="{{rootDirectory}}{{content.data}}" alt="entry photo"></a></span></div><div class="entry-text"><div class="entry-title">{{content.title}}</div><div class="entry-copy">{{content.description}}</div></div></div>';
	     var videoTemplate = '<div class="entry-video"><h2>&nbsp;</h2><div class="entry-vid"><iframe ng-src="{{content.data}}" width="280" height="200" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe></div><div class="entry-text"><div class="entry-title">{{content.title}}</div><div class="entry-copy">{{content.description}}</div></div></div>';
	     var noteTemplate = '<div class="entry-note"><h2>&nbsp;</h2><div class="entry-text"><div class="entry-title">{{content.title}}</div><div class="entry-copy">{{content.data}}</div></div></div>';

	     
	     var radioTemplate = '<div> <h2>{{content.question}}</h2><input type="hidden" name="question_{{content.id}}" value="{{content.id}}"/><label data-ng-repeat="answer in content.answer"><input type="radio" name="radio_{{content.id}}" ng-model="$parent.id"  value="{{answer.id}}" required="required"/> {{answer.label}} </label></div>';
	     
	     var radioTemplateFile = '/template/radiotpl.html';//'radiotpl.html';
	     var checkboxTemplateFile = '/template/checkboxtpl.html';
	     var imageTemplateFile = '/template/imagetpl.html';
	     
	     //radioTemplateFile = '/ang/radiotpl';
	      
	     
	     var getTemplate = function(contentType) {
	         var template = '';
	          
	         switch(contentType) {
	             case 'radio':
	                 template = radioTemplateFile;
	                 break;
	             case 'check':
	                 template = checkboxTemplateFile;
	                 break;
	             case 'image':
	                 template = imageTemplateFile;
	                 break;
	         }

	         return template;
	     }
	     
	     /**show tag html*/
	     var linker = function(scope, element, attrs) {
	    	 
	    	 scope.rootDirectory = 'images/';
	    	 //debugger;
	         element.html(getTemplate(scope.content.type) );//.show();

	         $compile(element.contents())(scope);
	     }
	     
	   
	     

	    /* EDITED FOR BREVITY */
	     
	     var directive = {};
	     directive.restrict = 'E';
	     //directive.link =  linker;	     
	     directive.template =  '<ng-include src="getTemplateUrl()"/>';
	     directive.controller = function($scope) {
	         $scope.getTemplateUrl = function() {  
	        	  
	        	 return getTemplate($scope.content.type);
	           
	         }
	       }
	     directive.scope  =  {
					             content:'=' 
					         }
	     
	     return directive;
	   /*
	     return {
	         restrict: "E",
	         link: linker,
	         scope: {
	             content:'='
	         }
	     };*/
	});