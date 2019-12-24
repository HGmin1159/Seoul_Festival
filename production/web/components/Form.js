const Form = ({searchHandler, prevHandler}) => {

  // Date.prototype.toDateInputValue = (function () {
  //   let local = new Date(this);
  //   local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
  //   return local.toJSON().slice(0, 10);
  // });

  return (
    <>
      <div className="dropdown">
        <span>축제검색: </span>
        <input type="text" onInput={e=>{
          searchHandler(e.target.value);
        }}></input>
        <br></br>
        <input type="checkbox" id="prev" onInput={e=>{
          prevHandler(e.target.checked);
        }}></input>
        <label htmlFor="prev">지난 축제</label>
        {/* <div className="dropdown-content">
          <label htmlFor="male">
            <input type="radio" name="gender" value="male" id="male"></input>
            남자
      </label>
          <label htmlFor="female">
            <input type="radio" name="gender" value="female" id="female"></input>
            여자
      </label><br></br>
          나이:
      <input type="text" id="age"></input><br></br>
          관심사:
      <input type="text" id="interest"></input><br></br>
          날짜:
      <input type="date" defaultValue={new Date().toDateInputValue()} id="date"></input><br></br>

          <button>축제 검색</button>
        </div> */}
        <style jsx>{`
          .dropdown {
            padding: 4%;
          }
        `}</style>
      </div>
    </>
  )
}

export default Form;