async function booking(form,attractionId) {
  let date = form.date.value;
  let time = form.querySelector("input[name='halfday']:checked").value;
  let prices = form.querySelector(".money").textContent;
  let token = localStorage.getItem("authToken");
  let takePrice = prices.split(" ")[1]; //新台幣 2000元
  let price = parseInt(takePrice); // 2000
 
  if (window.tokenResult  === null) { openDialog("login-dialog"); return;}
  
  let bookingData = {
    attractionId: attractionId,
    date: date,
    time: time,
    price: price
  };
  try{
    let res = await fetch("/api/booking",{
      method: "POST",
      headers:{
        "Content-Type": "application/json",
        "Authorization": `${token}`,
      },
      body:JSON.stringify(bookingData)
    })
    if (res.ok){
      window.location.href = "/booking";
      localStorage.setItem("cart",JSON.stringify(bookingData));

    }
  }catch (err){
    console.log(err.message);
    return err.message;
  }
}
