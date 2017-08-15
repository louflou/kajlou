drop table if exists customers cascade;
drop table if exists inventory cascade;
drop table if exists staff cascade;
drop table if exists sales cascade;
drop table if exists sales_details cascade;
drop table if exists products cascade;
drop table if exists supplier cascade;

create table customers(
	pno varchar not null,
	customer_name text not null,
	email text not null,
	address text not null,
	postno text not null,
	region text not null,
	primary key(pno)
);
create table products(
	product_id serial unique not null,
	product_name text not null,
	description text,
	brand text not null,
	price integer not null,
	category text not null,
	image text,
	active boolean not null,
	primary key(product_id)
);
create table staff(
	staff_id serial unique not null,
	title text not null,
	staff_name text not null,
	phone text not null,
	email text not null,
	primary key(staff_id)
);
create table supplier(
	supplier_name text not null,
	phone text not null,
	website text not null,
	primary key(supplier_name)
);
create table inventory(
	product_id integer not null references products,
	supplier text not null references supplier,
	product_cost integer not null,
	quantity integer not null,
	primary key(product_id, supplier)
);
create table sales_details(
	sales_id serial unique not null,
	customer_id varchar not null references customers,
	staff_id integer not null references staff,
	date date not null,
	discount integer not null,
	subtotal integer,
	primary key(sales_id)
);
create table sales(
	sales_id integer not null references sales_details,
	product_id integer not null references products,
	quantity integer not null,
	primary key(sales_id, product_id)
);
insert into staff (title, staff_name, phone, email) values
	('Manager', 'Louise Flou', '076-045 94 48', 'louise@flou.eu'),
	('Manager', 'Kajsa Araskoug', '076-207 22 48', 'kajsa.araskoug@gmail.com'),
	('Vendor', 'Henry Ford', '075-231 90 00', 'henry@mortfors-vv.com');
insert into customers (pno, customer_name, email, address, postno, region) values
	('880924-1723', 'Mikaela Arvidsson', 'mikkan__88@hotmail.com', 'Bäckahästgatan 35', '234 12', 'Malmö'),
	('791103-4551', 'Arvid Svensson', 'arvid.p.svensson@hotmail.com', 'Solbackevägen 7A', '213 13', 'Svalöv'),
	('910127-7840', 'Hanna Svärdh', 'svärdhiz_91@hotmail.com', 'Viskaregatan 26F', '253 60', 'Ramlösa')
	('861117-6521', 'Lisa Gran', 'gran@gmail.com', 'Granvägen 12', '124 12', 'Helsingborg');
insert into supplier(supplier_name, phone, website) values
	('Candy', '040-141202', 'http://www.candy-domestic.co.uk/'),
	('Elektrolux', '08-141614', 'http://www.electrolux.se/'),
	('WhiteAway', '040-139000', 'http://www.whiteaway.se/'),
	('Bosch', '040-120220', 'http://www.bosch.se/'),
	('Smeg', '045-340211', 'http://www.smeg.se/'),
	('Miele', '040-129054', 'https://www.miele.se/');
insert into products (product_name, description, brand, price, category, image, active) values
	('Candy Tvättmaskin', 'Utrusta ditt hushåll med denna kraftfulla tvättmaskin från Candy och njut av kvalitativa tvättresultat.', 'Candy', 2990, 'Tvättmaskin', 'https://tubby.scene7.com/is/image/tubby/CS1692D3?$prod_all4one$', true),

	('Electrolux FlexCare Tvättmaskin', 'Se till att dina kläder tvättas varsamt med denna tvättmaskin från Electrolux. Med AutoSense funktion och PowerJet teknik kan du enkelt justera tvättprocessen för att passa just dina behov.', 'Electrolux', 5795, 'Tvättmaskin', 'https://tubby.scene7.com/is/image/tubby/EW81611F?$prod_all4one$', true),

	('Bosch HomeConnect Tvättmaskin', 'Denna tvättmaskin tillhör energiklass A+++, som är den bästa på marknaden.', 'Bosch', 7950, 'Tvättmaskin', 'https://images.wagcdn.com/500/500/fill/p/prod_auto/frontbetjente-vaskemaskiner/wawh2668sn.jpg', true),

	('Sandstrøm Vinkyl', 'Vinkyl i elegant rostfri stål och stålhandtag för integrering eller placering under skåp. Energiklass C.', 'Sandstrøm', 6995, 'Kylskåp', 'https://tubby.scene7.com/is/image/tubby/SIWC46B15E?$prod_all4one$', true),

	('Smeg Colonial Spis', '60 cm bred gasspis i retrodesign som kommer att förgylla ditt kök. Energiklass A.', 'Smeg', 15995, 'Spis', 'https://tubby.scene7.com/is/image/tubby/CO68GMA8?$prod_all4one$', true),

	('Smeg diskmaskin (svart)', 'Diskmaskin med plats till 13 kuvert i tuff retrodesign från Smeg. Energiklass A+++.', 'Smeg', 11690, 'Diskmaskin', 'https://tubby.scene7.com/is/image/tubby/ST2FABNE2?$prod_all4one$', true),

	('Helintegrerad diskmaskin XXL', 'Höjdjusterbar överkorg, Standardprogram, t.ex. ECO, Automatic och Intensiv 75°C', 'Miele', 15300, 'Diskmaskin', 'https://www.miele.se/pmedia/30/Z17/20000130901-000-00_20000130901.jpg', false),

	('Bosch Vario Perfect Tvättmaskin', 'Maskinen har en kapacitet på 8 kg. Centrifugeringshastighet är upp till 1400 varv per minut. Det är en kolfri motor i tvättmaskinen. Har den bästa energiklassen på marknaden: A+++.', 'Bosch', 7490, 'Tvättmaskin', 'https://images.wagcdn.com/1200/1200/fill/p/prod_auto/frontbetjente-vaskemaskiner/wat286i8sn.jpg',  false);

insert into inventory (product_id, supplier, product_cost, quantity) values
	(1, 'Candy', 1500 ,8),
	(2, 'Elektrolux', 4000, 12),
	(3, 'WhiteAway', 4620, 2),
	(4, 'Bosch', 6350, 10),
	(5, 'WhiteAway', 6500, 5),
	(6, 'WhiteAway', 4495, 6),
	(7, 'Smeg', 12345, 9),
	(8, 'Smeg', 9995, 6),
	(9, 'Miele', 12400, 0),
	(10, 'Bosch', 5590, 2);

insert into sales_details(customer_id, staff_id, date, discount) values
	('791103-4551', 3, '2017-05-11', 0);

insert into sales(sales_id, product_id, quantity) values
	(1, 5, 1);

select * from inventory;
