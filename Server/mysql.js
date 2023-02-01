// const {createPool} = require('mysql2');

// const pool = createPool({
//     host:"localhost",
//     user:"root",
//     password:"root",
//     database:"fyp",
// });

// let sql = "UPDATE viewcount SET count = count + 1 where viewName = 'Gazing'";

// pool.execute(sql,(err,res)=>{
//     if(err)throw err;
//     console.log(res);
// })

module.exports = {
    connection: function () {
        const {createPool} = require('mysql2');

        const pool = createPool({
            host:"localhost",
            user:"root",
            password:"root",
            database:"fyp",
        });
    },
    updataNumberOfCus: function () {
        let sql = "UPDATE viewcount SET count = count + 1 where viewName = 'Gazing'";

        pool.execute(sql,(err,res)=>{
            if(err)throw err;
            console.log(res);
        })
        
    }
  };



