
#include<iostream>
#include<string>
#include"include/termcolor.hpp"
#include"include/builtin.hpp"






str next_player (str who_move){
if (who_move == "X") {
return "O";



}
else {
return "X";



}

};void draw_vert_border (bool endl = false){
log("|", endl);

};void draw_horz_border (){
log("+-+-+-+", true);

};void draw_row (str a, str b, str c){
draw_vert_border();
log(a);
draw_vert_border();
log(b);
draw_vert_border();
log(c);
draw_vert_border(true);

};void draw (str a, str b, str c, str d, str e, str f, str g, str h, str i){
draw_horz_border();
draw_row(a, b, c);
draw_horz_border();
draw_row(d, e, f);
draw_horz_border();
draw_row(g, h, i);
draw_horz_border();

};int ask_cell (str who_move){
log(who_move);
int cell = input<int>(" choose cell >>");

return cell;


};bool check_three (str a, str b, str c){
return a == b && b == c && c != " ";


};bool check_game_over (str a, str b, str c, str d, str e, str f, str g, str h, str i){
auto r1 = check_three(a, b, c);

auto r2 = check_three(a, d, g);

auto r3 = check_three(a, e, i);

auto r4 = check_three(b, e, h);

auto r5 = check_three(d, e, f);

auto r6 = check_three(g, e, c);

auto r7 = check_three(c, f, i);

auto r8 = check_three(g, h, i);

return r1 || r2 || r3 || r4 || r5 || r6 || r7 || r8;


};bool check_draw (str a, str b, str c, str d, str e, str f, str g, str h, str i){
return a != " " && b != " " && c != " " && d != " " && e != " " && f != " " && g != " " && h != " " && i != " ";


};



int main(){
    str a = " ";


str b = " ";


str c = " ";


str d = " ";


str e = " ";


str f = " ";


str g = " ";


str h = " ";


str i = " ";


str who_move = "X";


bool continue_game = true;


while (continue_game)
{
draw(a, b, c, d, e, f, g, h, i);

auto cell = ask_cell(who_move);


if (cell == 1) {
a = who_move;

}

else if (cell == 2) {
b = who_move;

}

else if (cell == 3) {
c = who_move;

}

else if (cell == 4) {
d = who_move;

}

else if (cell == 5) {
e = who_move;

}

else if (cell == 6) {
f = who_move;

}

else if (cell == 7) {
g = who_move;

}

else if (cell == 8) {
h = who_move;

}

else if (cell == 9) {
i = who_move;

}

else {
log_error("Enter number in range: 1 - 9!", true);
who_move = next_player(who_move);

}

auto game_over = check_game_over(a, b, c, d, e, f, g, h, i);


auto drw = check_draw(a, b, c, d, e, f, g, h, i);


if (game_over) {
draw(a, b, c, d, e, f, g, h, i);
log_info("Game Over! ");
log_info("Won: ");
log_info(who_move);
continue_game = false;

}

else if (drw) {
draw(a, b, c, d, e, f, g, h, i);
log_info("Draw!");
continue_game = false;

}

who_move = next_player(who_move);



}
;


}