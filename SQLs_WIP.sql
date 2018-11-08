SQL queries:

CREATE DATABASE credit_db;

BEGIN;
--
-- Create model Employee
--
CREATE TABLE `webapp_employee` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `first_name` varchar(30) NOT NULL, `last_name` varchar(30) NOT NULL, `email` varchar(254) NOT NULL, `point_recd` integer NOT NULL, `point_tosd` integer NOT NULL, `user_id_id` integer NOT NULL);
--
-- Create model Message
--
CREATE TABLE `webapp_message` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(80) NOT NULL, `content` varchar(240) NOT NULL);
--
-- Create model Redemption
--
CREATE TABLE `webapp_redemption` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `point_price` integer NOT NULL, `title` varchar(64) NOT NULL);
--
-- Create model Transaction
--
CREATE TABLE `webapp_transaction` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `points` integer NOT NULL, `pub_date` datetime(6) NOT NULL, `message_id` integer NOT NULL, `rdm_ID_id` integer NULL, `rec_ID_id` integer NOT NULL, `send_ID_id` integer NOT NULL);
ALTER TABLE `webapp_employee` ADD CONSTRAINT `webapp_employee_user_id_id_5989931c_fk_auth_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `webapp_transaction` ADD CONSTRAINT `webapp_transaction_message_id_e1a9d662_fk_webapp_message_id` FOREIGN KEY (`message_id`) REFERENCES `webapp_message` (`id`);
ALTER TABLE `webapp_transaction` ADD CONSTRAINT `webapp_transaction_rdm_ID_id_3ec42ff3_fk_webapp_redemption_id` FOREIGN KEY (`rdm_ID_id`) REFERENCES `webapp_redemption` (`id`);
ALTER TABLE `webapp_transaction` ADD CONSTRAINT `webapp_transaction_rec_ID_id_7f42fbdf_fk_webapp_employee_id` FOREIGN KEY (`rec_ID_id`) REFERENCES `webapp_employee` (`id`);
ALTER TABLE `webapp_transaction` ADD CONSTRAINT `webapp_transaction_send_ID_id_9cb5145d_fk_webapp_employee_id` FOREIGN KEY (`send_ID_id`) REFERENCES `webapp_employee` (`id`);
COMMIT;

BEGIN;
--
-- Alter field message on transaction
--
ALTER TABLE `webapp_transaction` DROP FOREIGN KEY `webapp_transaction_message_id_e1a9d662_fk_webapp_message_id`;
ALTER TABLE `webapp_transaction` MODIFY `message_id` integer NULL;
ALTER TABLE `webapp_transaction` ADD CONSTRAINT `webapp_transaction_message_id_e1a9d662_fk_webapp_message_id` FOREIGN KEY (`message_id`) REFERENCES `webapp_message` (`id`);
COMMIT;
BEGIN;


--
-- Create model Report
--
CREATE TABLE `webapp_report` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(100) NOT NULL, `sql_string` varchar(2048) NOT NULL);
COMMIT;


-- Since data are inserted into table by django framework, there is no sql queries records
-- I used Django API shell to create model objects (insert rows):
-- Ex. create new employee with foreign key on user 3
>>> from webapp.models import *
>>> u=User.objects.all()[3]
>>> e=Employee(first_name='John',last_name='Johnson'=,email='jojohnson@creditme.com',user_id=u) 
>>> # foreign key object is passed into method as object
>>> # point_recd and point_tosd has default value so no need to specify
>>> e=save()

-- I wrote a random data generator to generate random date. Using:
>>> import random
>>> t=Transaction(...)# ... some operation with random ...
>>> t.save()
-- Most of them are legal but some of them are not logical because of offset month range (30 days interval)
-- https://github.com/xs0203401/DMgtProject/blob/master/CreditMe/webapp/gen_rnd.py

-- Trigger:
-- This is a trigger checking legal trnsaction inserts
DELIMITER //
CREATE TRIGGER sanity_check_trans_before_insert BEFORE INSERT ON webapp_transaction FOR EACH ROW
BEGIN 
DECLARE pt_on_hand int;
SELECT point_recd FROM webapp_employee WHERE id = new.send_id_id INTO pt_on_hand;
IF pt_on_hand < new.points THEN 
  signal sqlstate -20000 SET msgtext = 'insufficient points!';
END IF;
IF new.rec_ID_id == new.send_id_id THEN BEGIN
IF new.rec_ID_id != 6 THEN 
  signal sqlstate -20000 SET msgtext = 'cannot give yourself points!';
end;
END IF; 
END IF;
END; //
DELIMITER ;
-- This is a trigger helps clean message table after transactions deleted
DELIMITER //
CREATE TRIGGER trans_after_delete_del_msg
AFTER DELETE ON webapp_transaction
BEGIN
IF old.message_id IS NOT NULL THEN 
  DELETE FROM webapp_message WHERE id = old.message_id;
END IF;
END; //
DELIMITER ;

-- Procedure:
DELIMITER //
CREATE procedure InsertNewTransNoMsg (
	IN Send_ID integer,
	IN Rec_ID integer,
	IN Points integer,
	)
BEGIN 
   INSERT INTO webapp_transaction (points, send_ID_id, rec_ID_id) VALUES (Points, Send_ID, Rec_ID);
END; //
DELIMITER ;



-- Report 1:
-- Aggregate usage of points for giving, receiving, and redemption, 
-- on monthly basis, also broken down by user, 
-- ranked in order of the most points received to least.
-- Since MySQL does NOT NOT NOT have outer join, 
-- I wrote several back to back left join union as views to overcome the problem
-- So I created views, and saved final sql_string for report retrieval (in the web):
create or replace view total_given_by_month_emp as
(select month(t.pub_date) as month, e.id as eid, e.first_name, e.last_name, sum(points) as total_given
from webapp_transaction t, webapp_employee e 
where e.id=t.send_id_id
and t.rec_ID_id!=6
and t.send_id_id!=6
and rdm_ID_id is null
group by month(t.pub_date), e.id);
create or replace view total_recd_by_month_emp as
(select month(t.pub_date) as month, e.id as eid, e.first_name, e.last_name, sum(points) as total_recd
from webapp_transaction t, webapp_employee e 
where e.id=t.rec_id_id
and t.rec_ID_id!=6
and t.send_id_id!=6
and rdm_ID_id is null
group by month(t.pub_date), e.id);
create or replace view total_redeem_by_month_emp as
(select month(t.pub_date) as month, e.id as eid, e.first_name, e.last_name, sum(points) as total_redeem
from webapp_transaction t, webapp_employee e 
where e.id=t.send_id_id
and rdm_ID_id is not null
group by month(t.pub_date), e.id);
create or replace view outer_gv_rc as
(select gv.eid, gv.month, gv.total_given, ifnull(rc.total_recd,0) total_recd
from total_given_by_month_emp gv left join total_recd_by_month_emp rc 
on gv.eid=rc.eid and gv.month=rc.month)
union
select rc.eid, rc.month, ifnull(gv.total_given,0) total_given, rc.total_recd
from total_recd_by_month_emp rc left join total_given_by_month_emp gv
on gv.eid=rc.eid and gv.month=rc.month;
create or replace view outer_gvrc_rd as
(select o.eid, o.month, o.total_given, o.total_recd, ifnull(rd.total_redeem,0) total_redeem
from outer_gv_rc o left join total_redeem_by_month_emp rd 
on o.eid=rd.eid and o.month=rd.month)
union
select rd.eid, rd.month, ifnull(o.total_given,0) total_given, ifnull(o.total_recd,0) total_recd, rd.total_redeem
from total_redeem_by_month_emp rd left join outer_gv_rc o
on o.eid=rd.eid and o.month=rd.month;
-- final sql:
select o.month, o.eid, e.first_name, e.last_name, e.email, o.total_given, o.total_recd, o.total_redeem
from outer_gvrc_rd o, webapp_employee e
where o.eid=e.id
order by o.total_recd desc;

-- Report 2:
-- Show who is not giving all points for the current month:
select e.id eid, e.first_name, e.last_name, e.email, sum(points) pt_gived_out
from webapp_transaction t, webapp_employee e
where t.send_id_id=e.id
and month(pub_date)=month(now())
and year(pub_date)=year(now())
and rdm_ID_id is null
and rec_ID_id!=6
and send_id_id!=6
group by send_id_id
having sum(points)<1000;

-- Report 3
-- Show all redemptions by month by user, for previous two month
select * from total_redeem_by_month_emp order by  month, eid;