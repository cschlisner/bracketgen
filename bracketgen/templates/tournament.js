$(document).on('ready', function() {
				
    var knownBrackets = [2,4,8,16,32], // Full Bracket Numbers (size = 2^n)

        // Placeholder variable names until we get Forms page done
        teams  = ["Player  1","Player  2","Player  3","Player  4","Player  5","Player  6","Player  7","Player  8","Player  9","Player 10",
                  "Player 11","Player 12","Player 13","Player 14","Player 15","Player 16","Player 17","Player 18","Player 19","Player 20",
                  "Player 21","Player 22","Player 23","Player 24","Player 25","Player 26","Player 27","Player 28","Player 29","Player 30",
                  "Player 31","Player 32"], 

        bracketCount = 0;

    // Creates Bracket Object with necessary match info
    function getBracket(base) {
                                                
        var closest 	= _.find(knownBrackets, function(k) { return k >= base; }),  // Closest 2^n size there
            extras 		= closest - base; // # of unfilled spaces on full bracket (2^n)

        if (extras > 0) // Use closest value for tournament generation
            base = closest;

        var brackets 	    = [], // Object - Saves all matches and info of tournament
            round 		    = 1, // Round one of tournament
            match_per_round = closest / 2, // # matches in first round (e.g.: if there are 16 participants, 8 matches occur in first round)
            teamIdx	        = 0, // Used to index "team" string array
            match_in_round  = 1; // Keeps place of which match w/in round tourney is in

        for (i = 1; i <= (base - 1); i++) { // Total number of games per tournament
            
            isextra = false; // 

            if (extras > 0) { // Eliminates top extra matches of the bracket in round 1 when #participants != full bracket size
                isextra = true;
                extras--;
            }

            // Used for choosing winner of past round to place in next round
            var last = _.map(_.filter(brackets, function(b) { return b.nextGame == i; }), 
                             function(b) { return {game: b.matchNo, teams: b.teamnames}; }); 
            
            // brackets Object (1 entry represents 1 match)
            brackets.push({
                // condition ? condition == true : condition == false
                lastGames:	round == 1 ? null : [last[0].game, last[1].game],
                nextGame:	i == (base - 1) ? null : (closest / 2) + Math.ceil(i / 2),
                teamnames:	round == 1 ? [teams[teamIdx], teams[teamIdx+1]] : ["",""],         
                                //[last[0].teams[_.random(1)],last[1].teams[_.random(1)]],
                matchNo:	i,
                roundNo:	round,
                extra:		isextra
            });
            
            // Next two names on the list of "teams"
            teamIdx += 2;
            match_in_round++; 
            
            // Move to next round condition
            if (match_in_round > match_per_round){
                round++;
                match_per_round /= 2;
                match_in_round = 1;
            }
            
        }

        renderBrackets(brackets);
            
    }

    // Creates tournament bracket on webpage
    function renderBrackets(struct) {
        
        var groupCount	= _.uniq(_.map(struct, function(s) { return s.roundNo; })).length; // Total number of rounds

        var group	= $('<div class="group'+(groupCount+1)+'" id="b'+bracketCount+'"></div>'),
            grouped = _.groupBy(struct, function(s) { return s.roundNo; }); // Sorts structure by roundNo
        
        for(g = 1; g <= groupCount; g++) { // Applies to each round of tournament
            var round = $('<div class="r'+g+'"></div>'); // Generate div for each round. Places appropriate bracketbox into round
            _.each(grouped[g], function(gg) {
                if(gg.extra)
                    round.append('<div></div>'); // Empty slot
                else
                    round.append('<div><div class="bracketbox"><span class="info">'+gg.matchNo+'</span><span class="teama">'+gg.teamnames[0]+'</span><span class="teamb">'+gg.teamnames[1]+'</span></div></div>');
            });
            group.append(round);
        }
        group.append('<div class="r'+(groupCount+1)+'"><div class="final"><div class="bracketbox"><span class="teamc">'+_.last(struct).teamnames[_.random(1)]+'</span></div></div></div>');
        $('#brackets').append(group);

        bracketCount++;
        $('html,body').animate({
            scrollTop: $("#b"+(bracketCount-1)).offset().top
        });
    }

    $('#add').on('click', function() {
        var opts = parseInt(prompt('Bracket size (number of teams):',32));

        if (!_.isNaN(opts) && opts <= _.last(knownBrackets))
            getBracket(opts);
        else
            alert('The bracket size you specified is not currently supported.');
    });

});