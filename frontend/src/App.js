import {BrowserRouter, Routes, Route} from "react-router-dom"
import { Main } from "./pages/Main";
import { Login } from "./pages/Login";
import { Signup } from "./pages/Signup";
import { MyPage } from "./pages/MyPage";
import { Navbar } from "./component/Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      
      <Routes>
        <Route path="/" exact element={<Main/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/signup" element={<Signup/>} />
        <Route path="/mypage" element={<MyPage/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
