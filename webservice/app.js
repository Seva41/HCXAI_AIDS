const express = require('express')
const bodyParser = require('body-parser');
const fs = require('fs');

const Router = express.Router()
Router.use("/",express.static("./MDCV-WebService"))
const app = express()

app.use("/",Router)
app.use(bodyParser.json());

const PORT = 5555;

/*=======================================================*/


app.get('/', function (req, res) {
  console.log("HA OCURRIDO UNA CONEXION DESDE ALGUN DISPOSITIVO...");
})

/* FILA CLIENTES */
app.post("/pushclientdone",(req,res)=>{
    let json = req.body
    let size = Object.keys(json).length;

    if(size !== 0){
        res.send({
            "json request size":size,
            "status":200,
            "info_json": "datainfo.json was created"
        })
        
        let file_name = `./MDCV-WebService/filaclientes/fila_clientes.txt`;
        
        if (fs.readFileSync(file_name, 'utf-8') == "ok"){
            fs.writeFile(file_name , `${json[0]["maquina"]}\n` ,function (err) {
                if(err){
                    console.error("ERROR DE ESCRITURA")
            console.error(err)
                }else{
                    console.log("/pushclientdone Fila clientes: ok :)");
                }
            })
        }else{
            fs.appendFile(file_name , `${json[0]["maquina"]}\n` ,function (err) {
                if(err){
                    console.error("ERROR DE ESCRITURA")
            console.error(err)
                }else{
                    console.log("/pushclientdone else: ok!");
                }
            })
        }

    }else{
        console.log("error");
        console.info(json)   
        res.send({
            "json request":json,
            "status":400
        })
    }
})

app.post("/pushserverdone",(req,res)=>{
    let json = req.body
    let size = Object.keys(json).length;

    if(size !== 0){
        res.send({
            "json request size":size,
            "status":200,
            "info_json": "datainfo.json was created"
        })

        let file_name = `./MDCV-WebService/filaclientes/fila_clientes.txt`;
        fs.writeFile(file_name , `${json[0]["server"]}` ,function (err) {
            if(err){
                console.error("ERROR DE ESCRITURA")
        console.error(err)
            }else{
                console.log("Fila clientes ok :)");
            }
        })
    }else{
        console.log("error");
        console.info(json)   
        res.send({
            "json request":json,
            "status":400
        })
    }
})


/* Classifier */
app.post("/pushdatanew",(req,res)=>{
    let json = req.body
    let size = Object.keys(json).length;
    if(size !== 0){
        res.send({
            "json request size":size,
            "status":200,
            "info_json": "datainfo.json was created"
        })
        let file_name = `./MDCV-WebService/plkpjhbx/${json[0]["maquina"]}.txt`;

        fs.writeFile(file_name, `Port: ${json[1]["Port"]}\t Tipo: ${json[1]["Tipo"]}\t Fecha: ${json[1]["Fecha"]}\t Hora: ${json[1]["Hora"]}\t IP: ${json[1]["IP"]}\n` ,function (err) {
            if(err){
                console.error("ERROR DE ESCRITURA")
		console.error(err)
            }else{
                console.log(`/pushdatanew: ${json[0]["maquina"]} ok :)`);
            }
        })
    }else{
        console.log("error");
        console.info(json)   
        res.send({
            "json request":json,
            "status":400
        })
    }
})

app.post("/pushdataappend",(req,res)=>{
    let json = req.body
    let size = Object.keys(json).length;
    if(size !== 0){
        res.send({
            "json request size":size,
            "status":200,
            "info_json": "datainfo.json was created"
        })
        let file_name = `./MDCV-WebService/plkpjhbx/${json[0]["maquina"]}.txt`;

        fs.appendFile(file_name, `Port: ${json[1]["Port"]}\tTipo: ${json[1]["Tipo"]}\tFecha: ${json[1]["Fecha"]}\t Hora: ${json[1]["Hora"]}\tIP: ${json[1]["IP"]}\n` ,function (err) {
            if(err){
                console.error("ERROR DE ESCRITURA")
		console.error(err)
            }else{
                console.log(`/pushdataappend: ${json[0]["maquina"]} ok :)`);
            }
        })


    }else{
        console.log("error");
        console.info(json)   
        res.send({
            "json request":json,
            "status":400
        })
    }
})

/* SERVER */
app.post("/pushplan",(req,res)=>{
    let json = req.body
    let size = Object.keys(json).length;

    if(size !== 0){
        res.send({
            "json request size":size,
            "status":200,
            "info_json": "datainfo.json was created"
        })

        for(const index in json){
            let file_name = `./MDCV-WebService/plans/${json[index]["maquina"]}.json`;
            fs.writeFile(file_name, JSON.stringify(json[index]) ,function (err) {
                if(err){
                    console.error("ERROR DE ESCRITURA")
            console.error(err)
                }else{
                    console.log(`/pushplan ${json[index]["maquina"]}.json ok :)`);
                }
            })
        }


    }else{
        console.log("error");
        console.info(json)   
        res.send({
            "json request":json,
            "status":400
        })
    }
})

app.post("/pushsintomas",(req,res)=>{
    let json = req.body
    let size = Object.keys(json).length;

    if(size !== 0){
        res.send({
            "json request size":size,
            "status":200,
            "info_json": "datainfo.json was created"
        })

        let file_name = `./MDCV-WebService/sintomas/${json[0]["maquina"]}.txt`;

        fs.appendFile(file_name, `Port: ${json[1]["Port"]}\tSintomas: ${json[1]["Sintoma"]}\n`,function (err) {
            if(err){
                console.error("ERROR DE ESCRITURA")
		console.error(err)
            }else{
                console.log(`/pushsintomas: ${json[0]["maquina"]}.txt ok :)`);
            }
        })

    }else{
        console.log("error");
        console.info(json)   
        res.send({
            "json request":json,
            "status":400
        })
    }
})
/* DJANGO */
app.post("/pushclientlogstats",(req,res)=>{
    let json = req.body
    let size = Object.keys(json).length;

    if(size !== 0){
        res.send({
            "json request size":size,
            "status":200,
            "info_json": "datainfo.json was created"
        })

        let file_name = `./MDCV-WebService/aidsclilogs/stats/${json[0]["maquina"]}.txt`;

        fs.appendFile(file_name, `Componente: ${json[1]["Componente"]}\tFuncion: ${json[1]["Funcion"]}\tFecha: ${json[1]["Fecha"]}\tHora: ${json[1]["Hora"]}\n`,function (err) {
            if(err){
                console.error("ERROR DE ESCRITURA")
		console.error(err)
            }else{
                console.log("Archivo /stats");
            }
        })

    }else{
        console.log("error");
        console.info(json)   
        res.send({
            "json request":json,
            "status":400
        })
    }
})

app.post("/pushclientlogtabla",(req,res)=>{
    let json = req.body
    let size = Object.keys(json).length;

    if(size !== 0){
        res.send({
            "json request size":size,
            "status":200,
            "info_json": "datainfo.json was created"
        })

        let file_name = `./MDCV-WebService/aidsclilogs/tabla/${json[0]["maquina"]}.txt`;

        fs.appendFile(file_name, `Funcion: ${json[1]["Funcion"]}\tPort: ${json[1]["Port"]}\tFecha: ${json[1]["Fecha"]}\tHora: ${json[1]["Hora"]}\tSintoma: ${json[1]["Sintoma"]}\n`,function (err) {
            if(err){
                console.error("ERROR DE ESCRITURA")
		console.error(err)
            }else{
                console.log("Archivo /tabla");
            }
        })

    }else{
        console.log("error");
        console.info(json)   
        res.send({
            "json request":json,
            "status":400
        })
    }
})

app.listen(PORT, function(){
    console.log("Server running in port " + PORT + "...");
});
