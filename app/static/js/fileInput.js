for (let el of document.getElementsByClassName("file-input"))
{
  el.addEventListener("change", (event) => {
    simplefilename = event.currentTarget.value.replace("C:\\fakepath\\", "");
    filenameSpan = event.currentTarget.nextElementSibling.nextElementSibling;
    if (filenameSpan.className !== "file-name")
    {
      throw new Error("Invalid taget");
    }
    filenameSpan.innerText = simplefilename;
  });
}