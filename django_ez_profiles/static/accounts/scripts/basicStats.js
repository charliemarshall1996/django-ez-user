

$.ajax({ 
    method: "GET", 
    url: userDataEndpoint, 
    success: function(data) {
      data = data.basic_stats
      displayBasicStat(data, 'interviewConversionRate');
      displayBasicStat(data, 'totalApplications');
      displayBasicStat(data, 'totalInterviews')
      console.log("drawing"); 
    }, 
    error: function(error_data) { 
      console.log(error_data); 
    } 
  }); 

    function displayBasicStat(data, id) {
        var statData = "";
        var statElement = document.getElementById(id);
        if (id == "interviewConversionRate") {
            statData = data.interview_conversion_rate;
        } else if (id == "totalApplications") {
            statData = data.total_jobs;
        } else {
            statData = data.total_interviewed_jobs;
        }
        if (statData == "") {
          statData = 0
        }
        statElement.innerHTML = statData;
    }
