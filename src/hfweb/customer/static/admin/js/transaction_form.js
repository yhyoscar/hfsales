
$(document).ready(function() {
    member_check();
});

function member_check(){
    x = document.getElementById('id_customer');
    if (x != null) {
        i = x.selectedIndex;
        if (x.options[i].text.includes("会员")) {
            if (document.getElementById("id_method").value == "AA") {
                disable_aa_payfor();
            }
            if (document.getElementById("id_payfor").value == "1") {
                disable_aa_method();
            }
            document.getElementById("id_method").onchange = function(){ 
                if (this.value == "AA") {
                    disable_aa_payfor();
                } else {
                    enable_aa_payfor();
                }
            };
            document.getElementById("id_payfor").onchange = function(){ 
                if (this.value == "1") {
                    disable_aa_method();
                } else {
                    enable_aa_method();
                }
            };
        } else {
            disable_aa_method();
            disable_aa_payfor();
        }

        x.onchange = function(){
            j = this.selectedIndex;
            if (x.options[j].text.includes("会员")) {
                enable_aa_method();
                enable_aa_payfor();
                document.getElementById("id_method").onchange = function(){
                    if (this.value == "AA") {
                        disable_aa_payfor();
                    } else {
                        enable_aa_payfor();
                    }
                };
                document.getElementById("id_payfor").onchange = function(){
                    if (this.value == "1") {
                        disable_aa_method();
                    } else {
                        enable_aa_method();
                    }
                };
            } else {
                disable_aa_method();
                disable_aa_payfor();
            }
        }
    }
}

function enable_aa_method(){
    document.querySelectorAll("#id_method option").forEach(opt => {
        if (opt.value == "AA") {
            opt.disabled = false;
        }
    });
}

function enable_aa_payfor(){
    document.querySelectorAll("#id_payfor option").forEach(opt => {
        if (opt.value == "1") {
            opt.disabled = false;
        }
    });
}

function disable_aa_method(){
    document.querySelectorAll("#id_method option").forEach(opt => {
        if (opt.value == "AA") {
            opt.disabled = true;
        }
    });
}

function disable_aa_payfor(){
    document.querySelectorAll("#id_payfor option").forEach(opt => {
        if (opt.value == "1") {
            opt.disabled = true;
        }
    });
}

