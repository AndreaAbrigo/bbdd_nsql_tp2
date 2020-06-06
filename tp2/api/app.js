var redis = require('redis');
var express = require('express')
var http = require("http");

var redisClient = redis.createClient(6379, 'redis');
var app = express()


redisClient.on('connect',function(){
    console.log('Conectado a Redis Server');
});

app.use(express.static('public'));
app.engine('html', require('ejs').renderFile);

app.get('/', function(req,res){
    var lista="episodios";
    console.log(lista)
    redisClient.lrange(lista, 0, -1, function(err, values){
        v=JSON.stringify(values)
        v=v.replace("[",'')
        v=v.replace("]",'')
        v=v.replace(/['"]+/g, '')
        console.log(v)
        var nombres = v.split(",");
        res.render('index.html', {nombres, lista})
    })
}) 

app.get('/nuevo/:nombreLista', function(req,res){
    var lista=req.params.nombreLista;
    res.render('cargarNuevo.html', {lista})
})

app.get('/cargarLista/:nombreLista/:valor', function(req,res){
    redisClient.lpush(req.params.nombreLista,req.params.valor)
    redisClient.lrange(req.params.nombreLista, 0, -1, function(err, values){
        res.send(JSON.stringify(values)) 
    }) 
})

app.get('/mostrarLista/:nombreLista', function(req,res){
    var lista=req.params.nombreLista;
    redisClient.lrange(req.params.nombreLista, 0, -1, function(err, values){
        v=JSON.stringify(values)
        v=v.replace("[",'')
        v=v.replace("]",'')
        v=v.replace(/['"]+/g, '')
        console.log(v)
        var nombres = v.split(",");
        res.render('index.html', {nombres, lista})
    })
}) 

app.get('/eliminarValor/:nombreLista/:valor', function(req,res){
    redisClient.lrem(req.params.nombreLista, 1, req.params.valor)
    redisClient.lrange(req.params.nombreLista, 0, -1, function(err, values){
        res.send(JSON.stringify(values)) 
    })
})

app.listen(3000, function(){
    console.log('Aplicación ejemplo, escuchando el puerto 3000')
})