var NPG = (function(){
	var ID_FEEDBACK_TEXTAREA = 'commentText';
	var ID_EDIT_TEXTAREA = 'wikitextareatext';

	$(document).ready(function(){
		highlightRowsOnHover();
		prepareFeedbackForm();
		updateFeedbackFormCount();
		useMarkItUp();
	});
	
	var highlightRowsOnHover = function(){
		$(".wikitext .wikilargelist tr").hover(
	      function () {
	        $(this).addClass("hoverRow");
	      }, 
	      function () {
			$(this).removeClass("hoverRow");
	      }
	    );
	};
	
	var prepareFeedbackForm = function (){
		$('#' + ID_FEEDBACK_TEXTAREA).bind('keyup', function(){
			updateFeedbackFormCount();
		});
	}
	
	var useMarkItUp = function(){
		if (!$('#' + ID_EDIT_TEXTAREA).attr('readonly')){
			$('#' + ID_EDIT_TEXTAREA).markItUp(mySettings_noble);
		}
	  
		$('#' + ID_FEEDBACK_TEXTAREA).markItUp(mySettings_bbcode);
  
	};
	
	var updateFeedbackFormCount = function(){
		var inputText = $('#' + ID_FEEDBACK_TEXTAREA).val();
		
		if (inputText){
			var letterCount = inputText.length;
			
			if (letterCount > 4000){ 
				inputText = inputText.substring(0,3999); 
				$('#' + ID_FEEDBACK_TEXTAREA).val(inputText); 
			}
			
			$('#showcount').val(letterCount);	
		}
	}
	
})();