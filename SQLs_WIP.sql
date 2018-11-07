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


-- Report 1
-- | id   | points | pub_date | message_id | rdm_ID_id | rec_ID_id | send_ID_id | id | first_name | last_name | email | point_recd | point_tosd | user_id_id |
select month(t.pub_date) as month, e.first_name, e.last_name, sum(points) as total_given
from webapp_transaction t, webapp_employee e 
where e.id=t.rec_id_id
and rdm_ID_id is null
group by month(t.pub_date), e.first_name, e.last_name
order by total_given desc;