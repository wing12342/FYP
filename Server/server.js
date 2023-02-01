var express = require('express');
var bodyParser = require('body-parser');
const fs = require('fs');
const { totalmem } = require('os');
const {createPool} = require('mysql2');

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

var rfid_list=[];

app.post("/shoppingcart", (req, res) => {

	var state = req.body;
	rfid_list = state.cart;
	console.log('rfid_getFromClient:'+rfid_list);
	res.json({ result: "Received" });
	if (rfid_list != "" ){
		let jsonContent = JSON.stringify(rfid_list);
		console.log('jsonContent:'+jsonContent);
		fs.writeFile('rfid_shoppingcart.json', jsonContent, 'utf8', function (err) {
			if (err) {
				console.log("An error occured while writing JSON Object to File.");
				return console.log(err);
			}		
			console.log("JSON file has been saved.");
		});
	}
});

app.post("/createNewOrder", async (req, res) => {

	var state = req.body.status;
	rfid_list = rfid_list.cart;
	console.log("state "+ state);
	res.json({ result: "Received" });

	state = true;
	//Reminds
	if(state){
		var id = req.body.memberID;
		let rawdata = fs.readFileSync('rfid_shoppingcart.json');
		let item = JSON.parse(rawdata);
		console.log("item:"+item);
		console.log("item0:"+item[0]);
		console.log("item1:"+item[1]);

		const pool = createPool({
			host:"localhost",
			user:"root",
			password:"root",
			database:"fyp",
		});

		getPrice = `SELECT item_detail.price FROM item JOIN item_detail ON item.itemDetailID = item_detail.itemDetailID Where item.rfid = '${item[0]}'`
		
		if(item.length>1){
			for (let i = 1; i < item.length; i++) {
				getPrice+= `OR item.rfid = '${item[i]}'`;
			}
		}
		
		const total = await new Promise((resolve) => {
			pool.execute(getPrice,(err,rows)=>{
				let total = 0;
				for (let i = 0; i < rows.length; i++) {
					console.log('price:'+rows[i]['price']);
					total += rows[i]['price'];
				}
				resolve(total);
				if(err)throw err;
				console.log('Total price:'+total);
			})
		})
		//Remind
		getAccount = `SELECT wallet FROM member WHERE memberID = '6'`;
		const account_bal = await new Promise((resolve) => {
			pool.execute(getAccount, (err, rows) => {
				let account_bal = rows[0]['wallet'];
				if(err)throw err;
				resolve(account_bal)
			})
		})
		console.log('account_bal:'+account_bal);

		new_bal = account_bal - total;
		update_bal = "UPDATE `fyp`.`member` SET `wallet` = " + new_bal + " WHERE `memberID` = 6"; 

		pool.execute(update_bal, (err, rows) => {
			if(err)throw err;
			console.log('update_bal:'+new_bal);
		})
	}
});

app.post("/getItem", (req, res) => {

	var state = req.body;
	let sql = "SELECT rfid FROM fyp.item_shelf Where shelfID = 1";
	const {createPool} = require('mysql2');
	const pool = createPool({
		host:"localhost",
		user:"root",
		password:"root",
		database:"fyp",
	});
	
	let sqlCommand = sql;
	pool.execute(sqlCommand,(err,result)=>{
		console.log(result);
		if(err)throw err;
		res.json(result);
	})
});

app.post("/rfidTest", (req, res) => {

	// Retrieve array form post body
	console.log(req.body);

	// Return json response
	res.json({ result: "Received" });
});


app.post("/gatestate", (req, res) => {

	// Retrieve array form post body
	var state = req.body.status;
	console.log(state);

	// Return json response
	res.json({ result: state });
});

app.post("/updataNumberOfCustomers", (req, res) => {

	// Retrieve array form post body
	var state = req.body;
	bodyParser.json(options);
	console.log(state);
	
	let sql = "UPDATE viewcount SET count = count + 1 where viewName = 'numberOfCustomers'";
	sqlCommand(sql);
	res.json({ result: "Received" });

});


// Server listening to PORT 3000
app.listen(3000);

function sqlCommand(sql) {
	const {createPool} = require('mysql2');

	const pool = createPool({
		host:"localhost",
		user:"root",
		password:"root",
		database:"fyp",
	});
	
	let sqlCommand = sql;
	pool.execute(sqlCommand,(err,res)=>{
		if(err)throw err;
		console.log(res);
	})
  }
