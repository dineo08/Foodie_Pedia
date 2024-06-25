document.getElementById("close_pop").addEventListener("click", ()=>{
    document.getElementById("popup").style.display = "none";
})

function getName(){
    document.getElementById("popup").style.display = "flex";
}

function submitName(){
    var recipe_name = document.getElementById("recipe_name").value
    console.log(recipe_name)
    if(recipe_name != null || recipe_name != ""){
        let forminfo = document.getElementById("title");
        let myForm = document.getElementById("myForm");
        forminfo.value = recipe_name;
        document.getElementById("popup").style.display = "none";
        //myForm.action ="{% url 'saverecipe' %}"
        myForm.submit();
    }
}

function confirmDelete(){
    var answer = window.confirm("Are you sure you want to delete" + recipe_id)

    if(answer){
        let myForm = document.getElementById("deleteForm");
        myForm.submit();
    }
}

function submitRecipeName(){
    var recipe_name = document.getElementById("recipe_name").value
    console.log(recipe_name)
    if(recipe_name != null || recipe_name != ""){
        let forminfo = document.getElementById("title");
        let myForm = document.getElementById("myForm");
        forminfo.value = recipe_name;
        document.getElementById("popup").style.display = "none";
        myForm.submit();
    }

}