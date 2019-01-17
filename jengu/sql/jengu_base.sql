/* create new lines in the revenues + unpayed tables every time a new user is added */
CREATE OR REPLACE FUNCTION insert_users_in_revenues()
  RETURNS trigger AS
$BODY$
BEGIN
 INSERT INTO jengu_revenues(owner_id,january,february,march,april,may,june,july,august,september,october,november,december)
 VALUES(NEW.id,0,0,0,0,0,0,0,0,0,0,0,0);
 INSERT INTO jengu_unpayed(owner_id,january,february,march,april,may,june,july,august,september,october,november,december)
 VALUES(NEW.id,0,0,0,0,0,0,0,0,0,0,0,0);
 RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER insert_users
AFTER INSERT 
ON auth_user
FOR EACH ROW 
EXECUTE PROCEDURE insert_users_in_revenues();


/* updates the monthly revenues / unpayed tables of the user every time 
	- he records a consultation
	- he updates the payement of a consultation */

CREATE OR REPLACE FUNCTION update_revenues()
  RETURNS trigger AS
$BODY$
	DECLARE
	BEGIN
	EXECUTE format (
		'UPDATE jengu_revenues 
              SET  %I = (
                SELECT SUM(payed) FROM jengu_consultations WHERE 
                    owner_id =  $1 AND to_char(date, ''MM-YYYY'') = $2 
                    )
				WHERE owner_id = $1'
		,to_char(NEW.date, 'FMmonth') )
	USING NEW.owner_id ,to_char(NEW.date, 'MM-YYYY');


	EXECUTE format (
		'UPDATE jengu_unpayed 
              SET  %I = (
                SELECT COUNT(id) FROM jengu_consultations WHERE 
                    owner_id =  $1 AND to_char(date, ''MM-YYYY'') = $2 
                    AND payed=0)
				WHERE owner_id = $1'
		,to_char(NEW.date, 'FMmonth') )
	USING NEW.owner_id ,to_char(NEW.date, 'MM-YYYY');
	
 RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER update_revenues
AFTER INSERT 
ON jengu_consultations
FOR EACH ROW 
EXECUTE PROCEDURE update_revenues();

CREATE TRIGGER update_revenues_correction
AFTER UPDATE 
ON jengu_consultations
FOR EACH ROW 
EXECUTE PROCEDURE update_revenues();

/* IMPORTANT : ADD A PROCEDURE TO ERASE THE CELL in the begining of the month (ROLLING YEARS) (with a cron job)*/

/* Erase profile and all its data */
CREATE OR REPLACE FUNCTION erase_user(i integer)
RETURNS void 
AS 
$$
BEGIN
DELETE FROM jengu_consultations WHERE owner_id=$1;
DELETE FROM jengu_patients WHERE owner_id = $1;
DELETE FROM jengu_revenues WHERE owner_id = $1;
DELETE FROM jengu_unpayed WHERE owner_id = $1;
DELETE FROM auth_user WHERE id = $1;
END;
$$ LANGUAGE plpgsql;
