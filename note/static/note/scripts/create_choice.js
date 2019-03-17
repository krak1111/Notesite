var choiceSwitch = document.getElementById("choice_switcher")
var SectionForm = document.getElementById("section_form")
var NoteForm = document.getElementById("note_form")


function changeForm(){
	if (choiceSwitch.checked) {
		SectionForm.style.display = "none";
		SectionForm.disabled = true;
		NoteForm.style.display = "blank";
		NoteForm.disabled = false;
	} else {
		SectionForm.style.display = "blank";
		SectionForm.disabled = true;
		NoteForm.style.display = "none";
		NoteForm.disabled = false;
	}
}
