# Nomenclature #

* SLICE - A 10px wide section. The basic unit of width.
* FLOOR - A 30px hight section. The basic unit of height.
* TILE - A background tile one FLOOR high and the full map width.

# Dimensions #

## Floor Height ##
A single floor is 40px high total. This breaks down to 10px of "flooring" and 30px of sprite area.
## Floor Width ##
All objects must be in increments of 10px wide, this is called a "slice". A single hotel room is 30px wide.

# Rendering #
Maps are done in tile/strips. One strip per floor.

http://wiki.gamedev.net/index.php/Scrolling_Games#Procedural_Backgrounds

## Move ##
When the frame of reference moves, we check if we have the tiles we need loaded, then load, then blit.
Next we blit in the flooring.
Last we blit in the objects.

## No Move ##
We just blit in the changes from the objects.

# Objects #
Objects are flexible and described in YAML, classed as follows:

* Lobby
* Office
* Housing
* Hotel
* Restaurant
* Store
* Entertainment
* Services
* Transportation

## Attributes ##
* Class
* Name
* Author
* Sprites
* Phases?
* Rent

## Scripting ##
Should we allow custom scripting? How much?

## Some Object Ideas ##
* Lobby
	* Floor lobby
	* Sky lobby
	* VIP Lobby?
* Office
	* Standard office
	* Call center
* Housing
	* Condo
* Hotel
	* Single room
	* Double room
	* Suite
	* Honeymoon suite
* Restaurant
	* Fast food
	** Burgers
	* Fine dining
* Store
	* Grocery Store
	* Pet shop
* Entertainment
	* Movie theater
* Services
	* Trash
	* Medical
	* Parking
* Transportation
	* Stairs
	* Elevator
	* Escalator
	* Express Elevator

# People #
People are typed as well. They are randomly generated and have traits.

* Office worker
* Family member (for housing)
* Visitor (for shops, entertainment, hotel, food)

# Time Scale #
We will work monthly as in Yoot tower, instead of quarters.

* 12 Months, 5 weekdays, 1 weekend in each.
* Each spin of the loop is a 5 minute block == 288 frames a "day"
* You can speed it up/slow it down as much as you want.
* By default each frame is 0.10 long
