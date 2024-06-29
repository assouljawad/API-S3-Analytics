import express from "express"

const app = express()
app.use(express.json());
const PORT = 3000

app.get("/", (req, res)=>{
    res.send("hello world")
    console.log(req.method);
    res.status(200)
})
app.post("/", (req, res)=>{
   const data = req.body
   console.log(req.method);
    res.send(data)
    res.end()
})

app.listen(3000,()=>{
console.log("The Server is running on port", PORT);
})



