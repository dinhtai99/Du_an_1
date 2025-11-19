const products = [
  { name: "Laptop", price: 2000 },
  { name: "Phone", price: 1000 },
  { name: "Tablet", price: 1500 },
];

// a. Tạo mảng expensive gồm sản phẩm có giá > 1500
const expensive = products.filter(product => product.price > 1500);

console.log("a. Mảng expensive (sản phẩm có giá > 1500):");
console.log(expensive);

// b. In tên các sản phẩm trong products bằng for…of
console.log("\nb. Tên các sản phẩm:");
for (const product of products) {
  console.log(product.name);
}

// ============================================
// Bài tập 2: Spread và Rest
// ============================================

// a. Dùng spread tạo mảng mới
const arr1 = [1, 2];
const arr2 = [3, 4];
const arr3 = [...arr1, ...arr2];

console.log("\n\na. Mảng arr3 (dùng spread):");
console.log("arr3 =", arr3);

// b. Viết hàm dùng rest để trả về tích tất cả tham số
function multiply(...nums) {
  return nums.reduce((product, num) => product * num, 1);
}

console.log("\nb. Hàm multiply với rest parameter:");
console.log("multiply(2, 3, 4) =", multiply(2, 3, 4));
console.log("multiply(1, 2, 3, 4, 5) =", multiply(1, 2, 3, 4, 5));
console.log("multiply(5, 10) =", multiply(5, 10));

// ============================================
// Bài tập 3: Optional Chaining + AND && + OR ||
// ============================================

const user = {
  profile: {
    email: "test@gmail.com",
  }
};

// 1. Lấy ra email bằng optional chaining
const email = user?.profile?.email;
console.log("\n\n1. Email (dùng optional chaining):");
console.log("Email:", email);

// 2. Lấy ra phone, nếu không có thì nhận giá trị là "Chưa cập nhật" (dùng ||)
const phone = user?.profile?.phone || "Chưa cập nhật";
console.log("\n2. Phone (dùng ||):");
console.log("Phone:", phone);

// 3. Nếu có profile thì in "Có thông tin hồ sơ" (dùng &&)
user?.profile && console.log("\n3. Có thông tin hồ sơ");

// ============================================
// Bài tập 4: Map - Chỉ giữ điểm cao nhất
// ============================================

const scores = [
  ["An", 7],
  ["Bình", 9],
  ["An", 8],
  ["Chi", 8.5],
];

// Tạo Map chỉ giữ điểm cao nhất của mỗi sinh viên
const scoreMap = new Map();

for (const [name, score] of scores) {
  // Nếu sinh viên chưa có trong Map, thêm vào
  // Nếu đã có, chỉ cập nhật nếu điểm mới cao hơn
  if (!scoreMap.has(name) || score > scoreMap.get(name)) {
    scoreMap.set(name, score);
  }
}

console.log("\n\nMap điểm cao nhất của mỗi sinh viên:");
for (const [name, score] of scoreMap) {
  console.log(`${name}: ${score}`);
}

// ============================================
// Bài tập 5: Optional Chaining + Spread với Classes
// ============================================

const classes = [
  { id: 1, name: "JS", students: ["An", "Bình"] },
  { id: 2, name: "React", students: null },
];

// 1. Dùng optional chaining lấy danh sách sinh viên của class id=2, nếu null trả về mảng rỗng []
const class2 = classes.find(c => c.id === 2);
const studentsClass2 = class2?.students ?? [];
console.log("\n\n1. Danh sách sinh viên class id=2 (dùng optional chaining):");
console.log("students:", studentsClass2);

// 2. Dùng spread để thêm "Chi" vào danh sách sinh viên của class id=1 mà không sửa trực tiếp dữ liệu gốc
const class1 = classes.find(c => c.id === 1);
const studentsClass1WithChi = [...(class1?.students || []), "Chi"];
console.log("\n2. Danh sách sinh viên class id=1 sau khi thêm 'Chi' (dùng spread, không sửa dữ liệu gốc):");
console.log("Danh sách mới:", studentsClass1WithChi);
console.log("Danh sách gốc (không đổi):", class1?.students);

// ============================================
// Các cách thay thế cho filter()
// ============================================

const products2 = [
  { name: "Laptop", price: 2000 },
  { name: "Phone", price: 1000 },
  { name: "Tablet", price: 1500 },
];

console.log("\n\n=== CÁC CÁCH THAY THẾ CHO filter() ===");

// Cách 1: Dùng for...of loop
const expensive1 = [];
for (const product of products2) {
  if (product.price > 1500) {
    expensive1.push(product);
  }
}
console.log("\n1. Dùng for...of loop:");
console.log("mang co gia tren 1500 la:", expensive1);

// Cách 2: Dùng for loop thông thường
const expensive2 = [];
for (let i = 0; i < products2.length; i++) {
  if (products2[i].price > 1500) {
    expensive2.push(products2[i]);
  }
}
console.log("\n2. Dùng for loop thông thường:");
console.log("mang co gia tren 1500 la:", expensive2);

// Cách 3: Dùng forEach
const expensive3 = [];
products2.forEach(product => {
  if (product.price > 1500) {
    expensive3.push(product);
  }
});
console.log("\n3. Dùng forEach:");
console.log("mang co gia tren 1500 la:", expensive3);

// Cách 4: Dùng reduce
const expensive4 = products2.reduce((acc, product) => {
  if (product.price > 1500) {
    acc.push(product);
  }
  return acc;
}, []);
console.log("\n4. Dùng reduce:");
console.log("mang co gia tren 1500 la:", expensive4);

// Cách 5: Dùng map kết hợp với filter logic (không khuyến khích)
const expensive5 = products2.map(product => {
  return product.price > 1500 ? product : null;
}).filter(item => item !== null);
console.log("\n5. Dùng map kết hợp filter (không khuyến khích):");
console.log("mang co gia tren 1500 la:", expensive5);

// ============================================
// Các cách thay thế cho reduce() trong hàm multiply
// ============================================

console.log("\n\n=== CÁC CÁCH THAY THẾ CHO reduce() TRONG HÀM multiply ===");

// Cách 1: Dùng for...of loop
function multiply1(...nums) {
  let product = 1;
  for (const num of nums) {
    product *= num;
  }
  return product;
}
console.log("\n1. Dùng for...of loop:");
console.log("multiply1(2, 3, 4) =", multiply1(2, 3, 4));

// Cách 2: Dùng for loop thông thường
function multiply2(...nums) {
  let product = 1;
  for (let i = 0; i < nums.length; i++) {
    product *= nums[i];
  }
  return product;
}
console.log("\n2. Dùng for loop thông thường:");
console.log("multiply2(2, 3, 4) =", multiply2(2, 3, 4));

// Cách 3: Dùng forEach
function multiply3(...nums) {
  let product = 1;
  nums.forEach(num => {
    product *= num;
  });
  return product;
}
console.log("\n3. Dùng forEach:");
console.log("multiply3(2, 3, 4) =", multiply3(2, 3, 4));

// Cách 4: Dùng while loop
function multiply4(...nums) {
  let product = 1;
  let i = 0;
  while (i < nums.length) {
    product *= nums[i];
    i++;
  }
  return product;
}
console.log("\n4. Dùng while loop:");
console.log("multiply4(2, 3, 4) =", multiply4(2, 3, 4));

// Cách 5: Dùng đệ quy (recursion)
function multiply5(...nums) {
  if (nums.length === 0) return 1;
  if (nums.length === 1) return nums[0];
  return nums[0] * multiply5(...nums.slice(1));
}
console.log("\n5. Dùng đệ quy (recursion):");
console.log("multiply5(2, 3, 4) =", multiply5(2, 3, 4));

