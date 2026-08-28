.class public Lpmsj/work/b/v;
.super Lpmsj/work/b/n;


# static fields
.field public static B:Lpmsj/work/a/i;

.field public static C:Lpmsj/work/a/i;

.field public static D:Lpmsj/work/a/i;

.field public static final I:[S

.field private static L:Lpmsj/work/a/i;

.field private static M:Lpmsj/work/a/i;

.field private static N:Lpmsj/work/a/i;


# instance fields
.field protected A:Lpmsj/work/a/b;

.field public E:Lpmsj/work/b/u;

.field public F:I

.field public G:I

.field public H:Z

.field protected J:Lpmsj/work/b/n;

.field private K:Lpmsj/work/a/i;

.field private O:I

.field private P:Ljava/lang/String;

.field private Q:I

.field private R:Ljava/lang/String;

.field private S:I

.field private final h:I

.field private i:Ljava/lang/StringBuffer;


# direct methods
.method static constructor <clinit>()V
    .locals 6

    const/4 v5, 0x2

    const/4 v4, 0x1

    const/4 v3, 0x0

    const v2, 0x57c148

    const v1, 0x552c4f

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v1, v3}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, Lpmsj/work/b/v;->B:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v1, v4}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, Lpmsj/work/b/v;->C:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v1, v5}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, Lpmsj/work/b/v;->D:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v2, v3}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, Lpmsj/work/b/v;->L:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v2, v4}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, Lpmsj/work/b/v;->M:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v2, v5}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, Lpmsj/work/b/v;->N:Lpmsj/work/a/i;

    const/16 v0, 0xd

    new-array v0, v0, [S

    fill-array-data v0, :array_0

    sput-object v0, Lpmsj/work/b/v;->I:[S

    return-void

    nop

    :array_0
    .array-data 2
        0xf1s
        0xdcs
        0x122s
        0xe7s
        0x118s
        0xfas
        0x10es
        0x10fs
        0xf2s
        0xf0s
        0x104s
        0xdds
        0xe6s
    .end array-data
.end method

.method public constructor <init>(IBIIZ)V
    .locals 5

    const/4 v4, 0x4

    const/4 v3, 0x0

    const/4 v2, 0x1

    invoke-direct {p0, p1, p3, v2, p5}, Lpmsj/work/b/n;-><init>(IIZZ)V

    sget v0, Lpmsj/work/a/c;->F:I

    iput v0, p0, Lpmsj/work/b/v;->F:I

    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v0}, Ljavax/microedition/lcdui/Font;->e()I

    move-result v0

    iput v0, p0, Lpmsj/work/b/v;->h:I

    iput v3, p0, Lpmsj/work/b/v;->O:I

    iput-byte p2, p0, Lpmsj/work/b/v;->n:B

    const v0, 0x186a0

    div-int v0, p3, v0

    if-ne v2, v0, :cond_0

    invoke-virtual {p0, p4}, Lpmsj/work/b/v;->y(I)V

    rem-int/lit8 v0, p4, 0x2

    int-to-byte v0, v0

    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-eqz v1, :cond_0

    if-ne v2, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/16 v1, 0x3a99

    invoke-virtual {v0, v4, v1}, La/a/d;->a(II)V

    :cond_0
    :goto_0
    sget-object v0, Lpmsj/work/a/c;->v:[I

    aget v0, v0, v3

    iput v0, p0, Lpmsj/work/b/v;->s:I

    iput v3, p0, Lpmsj/work/b/v;->t:I

    iput-byte v2, p0, Lpmsj/work/b/v;->g:B

    return-void

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/16 v1, 0x3a98

    invoke-virtual {v0, v4, v1}, La/a/d;->a(II)V

    goto :goto_0
.end method

.method public static H(I)I
    .locals 2

    const v1, 0x186a0

    if-nez p0, :cond_0

    move v0, v1

    :goto_0
    return v0

    :cond_0
    rem-int/lit16 v0, p0, 0x2710

    div-int/lit16 v0, v0, 0x3e8

    add-int/lit8 v0, v0, 0x1

    mul-int/lit16 v0, v0, 0x3e8

    add-int/2addr v0, v1

    goto :goto_0
.end method

.method protected static K(I)I
    .locals 2

    div-int/lit16 v0, p0, 0x3e8

    const/16 v1, 0xb

    sub-int/2addr v0, v1

    return v0
.end method

.method public static L(I)I
    .locals 1

    rem-int/lit16 v0, p0, 0x3e8

    div-int/lit8 v0, v0, 0x64

    add-int/lit8 v0, v0, 0x20

    return v0
.end method

.method private a(Ljava/lang/String;)I
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/v;->P:Ljava/lang/String;

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    iput-object p1, p0, Lpmsj/work/b/v;->P:Ljava/lang/String;

    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v0, p1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lpmsj/work/b/v;->Q:I

    :cond_0
    iget v0, p0, Lpmsj/work/b/v;->Q:I

    return v0
.end method

.method private a()V
    .locals 5

    const/4 v4, 0x2

    const/4 v3, 0x1

    const/4 v2, 0x0

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-eqz v0, :cond_1

    iget-byte v0, p0, Lpmsj/work/b/v;->n:B

    if-ne v4, v0, :cond_2

    move v0, v3

    :goto_0
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    iget v1, v1, La/a/d;->b:I

    if-eq v1, v0, :cond_0

    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v1, v0}, La/a/d;->d(I)V

    :cond_0
    iget-byte v0, p0, Lpmsj/work/b/v;->n:B

    if-ne v3, v0, :cond_3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v0, v4}, La/a/d;->a(B)V

    :cond_1
    :goto_1
    return-void

    :cond_2
    move v0, v2

    goto :goto_0

    :cond_3
    const/4 v0, 0x3

    iget-byte v1, p0, Lpmsj/work/b/v;->n:B

    if-ne v0, v1, :cond_1

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v0, v2}, La/a/d;->a(B)V

    goto :goto_1
.end method

.method private b(I)V
    .locals 1

    iput p1, p0, Lpmsj/work/b/v;->F:I

    const/4 v0, 0x0

    iput v0, p0, Lpmsj/work/b/v;->G:I

    return-void
.end method

.method public static u(I)Ljava/lang/String;
    .locals 1

    sget-object v0, Lpmsj/work/a/c;->aB:[Ljava/lang/String;

    array-length v0, v0

    if-lt p0, v0, :cond_0

    const-string v0, ""

    :goto_0
    return-object v0

    :cond_0
    sget-object v0, Lpmsj/work/a/c;->aB:[Ljava/lang/String;

    aget-object v0, v0, p0

    goto :goto_0
.end method

.method public static v(I)Ljava/lang/String;
    .locals 1

    sget-object v0, Lpmsj/work/a/c;->aM:[Ljava/lang/String;

    array-length v0, v0

    if-lt p0, v0, :cond_0

    const-string v0, ""

    :goto_0
    return-object v0

    :cond_0
    sget-object v0, Lpmsj/work/a/c;->aM:[Ljava/lang/String;

    aget-object v0, v0, p0

    goto :goto_0
.end method

.method public static w(I)Ljava/lang/String;
    .locals 1

    sparse-switch p0, :sswitch_data_0

    const-string v0, ""

    :goto_0
    return-object v0

    :sswitch_0
    const-string v0, "\u5e2e\u4e3b"

    goto :goto_0

    :sswitch_1
    const-string v0, "\u5e2e\u4f17"

    goto :goto_0

    :sswitch_data_0
    .sparse-switch
        0xc8 -> :sswitch_1
        0x3e8 -> :sswitch_0
    .end sparse-switch
.end method

.method public static x(I)B
    .locals 1

    rem-int/lit8 v0, p0, 0x2

    int-to-byte v0, v0

    return v0
.end method


# virtual methods
.method public final A()V
    .locals 1

    invoke-super {p0}, Lpmsj/work/b/n;->A()V

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    invoke-virtual {p0}, Lpmsj/work/b/v;->r()V

    invoke-virtual {p0}, Lpmsj/work/b/v;->I()V

    goto :goto_0
.end method

.method public final A(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    if-nez p1, :cond_1

    const/4 v0, 0x0

    :goto_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v2, 0x5

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0

    :cond_1
    add-int/lit16 v0, p1, 0x3e80

    goto :goto_1
.end method

.method public final B(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    if-nez p1, :cond_1

    const/4 v0, 0x0

    :goto_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v2, 0x6

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0

    :cond_1
    add-int/lit16 v0, p1, 0x4268

    goto :goto_1
.end method

.method public final C(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    if-nez p1, :cond_1

    const/4 v0, 0x0

    :goto_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v2, 0x7

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0

    :cond_1
    add-int/lit16 v0, p1, 0x4650

    goto :goto_1
.end method

.method public final D(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    if-nez p1, :cond_1

    const/4 v0, 0x0

    :goto_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/16 v2, 0x8

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0

    :cond_1
    add-int/lit16 v0, p1, 0x4a38

    goto :goto_1
.end method

.method public final E(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    if-nez p1, :cond_1

    const/4 v0, 0x0

    :goto_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/16 v2, 0x9

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0

    :cond_1
    add-int/lit16 v0, p1, 0x4e20

    goto :goto_1
.end method

.method public final F()La/a/d;
    .locals 3

    invoke-super {p0}, Lpmsj/work/b/n;->F()La/a/d;

    move-result-object v0

    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-eqz v1, :cond_0

    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v1}, La/a/d;->b()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {v0, v1}, La/a/d;->a(Ljava/util/Vector;)V

    const v1, 0x186a0

    iget v2, p0, Lpmsj/work/b/v;->u:I

    if-ne v1, v2, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/v;->C()I

    move-result v1

    invoke-virtual {v0, v1}, La/a/d;->d(I)V

    :cond_0
    return-object v0
.end method

.method public final F(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    if-nez p1, :cond_1

    const/4 v0, 0x0

    :goto_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/16 v2, 0xa

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0

    :cond_1
    add-int/lit16 v0, p1, 0x5208

    goto :goto_1
.end method

.method public final G(I)V
    .locals 4

    const/4 v3, 0x0

    const v0, 0x186a0

    iget v1, p0, Lpmsj/work/b/v;->u:I

    if-ne v0, v1, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-eqz v0, :cond_0

    const v0, 0x18a88

    iget v1, p0, Lpmsj/work/b/v;->u:I

    if-ne v0, v1, :cond_2

    move v0, v3

    :goto_1
    const/4 v1, 0x3

    if-ge v0, v1, :cond_2

    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    add-int/lit8 v2, v0, 0x20

    invoke-virtual {v1, v2, v3}, La/a/d;->a(II)V

    add-int/lit8 v0, v0, 0x1

    goto :goto_1

    :cond_2
    if-eqz p1, :cond_0

    invoke-static {p1}, Lpmsj/work/b/v;->L(I)I

    move-result v0

    iget v1, p0, Lpmsj/work/b/v;->u:I

    const v2, 0x18e70

    if-lt v1, v2, :cond_3

    add-int/lit8 v0, v0, 0x1

    :cond_3
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const v2, 0x9c40

    rem-int/lit16 v3, p1, 0x2710

    add-int/2addr v2, v3

    invoke-virtual {v1, v0, v2}, La/a/d;->a(II)V

    goto :goto_0
.end method

.method public final I()V
    .locals 3

    const/4 v2, 0x0

    iget v0, p0, Lpmsj/work/b/v;->u:I

    sparse-switch v0, :sswitch_data_0

    iget v0, p0, Lpmsj/work/b/v;->u:I

    const v1, 0x18e70

    if-lt v0, v1, :cond_1

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v0, v2}, La/a/d;->d(I)V

    const/4 v0, 0x3

    iget-byte v1, p0, Lpmsj/work/b/v;->n:B

    if-ne v0, v1, :cond_2

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v1, 0x2

    invoke-virtual {v0, v1}, La/a/d;->a(B)V

    :cond_0
    :goto_0
    iput-boolean v2, p0, Lpmsj/work/b/v;->y:Z

    :cond_1
    :goto_1
    return-void

    :sswitch_0
    invoke-super {p0}, Lpmsj/work/b/n;->I()V

    goto :goto_1

    :sswitch_1
    invoke-direct {p0}, Lpmsj/work/b/v;->a()V

    goto :goto_0

    :cond_2
    const/4 v0, 0x1

    iget-byte v1, p0, Lpmsj/work/b/v;->n:B

    if-ne v0, v1, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v0, v2}, La/a/d;->a(B)V

    goto :goto_0

    nop

    :sswitch_data_0
    .sparse-switch
        0x186a0 -> :sswitch_0
        0x18a88 -> :sswitch_1
    .end sparse-switch
.end method

.method public final I(I)V
    .locals 2

    const v1, 0x186a0

    if-eqz p1, :cond_2

    invoke-static {p1}, Lpmsj/work/b/v;->H(I)I

    move-result v0

    iget v1, p0, Lpmsj/work/b/v;->u:I

    if-eq v0, v1, :cond_1

    iput v0, p0, Lpmsj/work/b/v;->u:I

    invoke-virtual {p0}, Lpmsj/work/b/v;->A()V

    :cond_0
    :goto_0
    return-void

    :cond_1
    invoke-virtual {p0, p1}, Lpmsj/work/b/v;->G(I)V

    goto :goto_0

    :cond_2
    iget v0, p0, Lpmsj/work/b/v;->u:I

    if-eq v1, v0, :cond_0

    iput v1, p0, Lpmsj/work/b/v;->u:I

    invoke-virtual {p0}, Lpmsj/work/b/v;->A()V

    goto :goto_0
.end method

.method public final J()V
    .locals 3

    const/4 v2, 0x1

    iget v0, p0, Lpmsj/work/b/v;->u:I

    sparse-switch v0, :sswitch_data_0

    iget v0, p0, Lpmsj/work/b/v;->u:I

    const v1, 0x18e70

    if-lt v0, v1, :cond_1

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v0, v2}, La/a/d;->d(I)V

    const/4 v0, 0x3

    iget-byte v1, p0, Lpmsj/work/b/v;->n:B

    if-ne v0, v1, :cond_2

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v1, 0x2

    invoke-virtual {v0, v1}, La/a/d;->a(B)V

    :cond_0
    :goto_0
    iput-boolean v2, p0, Lpmsj/work/b/v;->y:Z

    :cond_1
    :goto_1
    return-void

    :sswitch_0
    invoke-super {p0}, Lpmsj/work/b/n;->J()V

    goto :goto_1

    :sswitch_1
    invoke-direct {p0}, Lpmsj/work/b/v;->a()V

    goto :goto_0

    :cond_2
    iget-byte v0, p0, Lpmsj/work/b/v;->n:B

    if-ne v2, v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, La/a/d;->a(B)V

    goto :goto_0

    nop

    :sswitch_data_0
    .sparse-switch
        0x186a0 -> :sswitch_0
        0x18a88 -> :sswitch_1
    .end sparse-switch
.end method

.method public final J(I)V
    .locals 3

    if-eqz p1, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/16 v1, 0x20

    const v2, 0x9c40

    add-int/2addr v2, p1

    invoke-virtual {v0, v1, v2}, La/a/d;->a(II)V

    :cond_0
    return-void
.end method

.method public K()Z
    .locals 6

    const/4 v5, 0x0

    iget-byte v0, p0, Lpmsj/work/b/v;->e:B

    iget-byte v1, p0, Lpmsj/work/b/v;->f:B

    iget-object v2, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    if-eqz v2, :cond_4

    iget-object v2, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    invoke-virtual {v2}, Lpmsj/work/b/n;->K()Z

    move-result v2

    :goto_0
    invoke-super {p0}, Lpmsj/work/b/n;->K()Z

    move-result v3

    iget-object v4, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    if-eqz v4, :cond_2

    if-eqz v3, :cond_2

    invoke-virtual {p0}, Lpmsj/work/b/v;->M()Z

    move-result v4

    if-eqz v4, :cond_2

    iget-object v4, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    iget-byte v4, v4, Lpmsj/work/b/n;->e:B

    if-ne v4, v0, :cond_0

    iget-object v4, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    iget-byte v4, v4, Lpmsj/work/b/n;->f:B

    if-eq v4, v1, :cond_1

    :cond_0
    iget-object v4, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    invoke-virtual {v4, v0, v1}, Lpmsj/work/b/n;->c(II)V

    :cond_1
    iget-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    iget-byte v1, p0, Lpmsj/work/b/v;->e:B

    iget-byte v4, p0, Lpmsj/work/b/v;->f:B

    invoke-virtual {v0, v1, v4, v5}, Lpmsj/work/b/n;->b(IIZ)I

    :cond_2
    if-eqz v2, :cond_3

    iget-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    invoke-virtual {v0}, Lpmsj/work/b/n;->M()Z

    move-result v0

    if-nez v0, :cond_3

    iget-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    invoke-virtual {v0}, Lpmsj/work/b/n;->I()V

    :cond_3
    return v3

    :cond_4
    move v2, v5

    goto :goto_0
.end method

.method public final L()Z
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    invoke-virtual {v0}, Lpmsj/work/b/n;->L()Z

    move-result v0

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    invoke-super {p0}, Lpmsj/work/b/n;->L()Z

    move-result v0

    goto :goto_0
.end method

.method public final M(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    const/16 v0, 0x32c8

    const/4 v1, 0x1

    rem-int/lit8 v2, p1, 0x2

    int-to-byte v2, v2

    if-ne v1, v2, :cond_1

    add-int/lit8 v0, v0, 0x1

    :cond_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v2, 0x2

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0
.end method

.method public final P()V
    .locals 4

    const/16 v3, 0x9

    const/4 v2, 0x6

    invoke-virtual {p0, v3}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    if-eqz v0, :cond_0

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v1, v3}, Lpmsj/work/b/v;->f(B)I

    move-result v1

    if-ne v0, v1, :cond_0

    sget-object v0, Lpmsj/work/a/c;->v:[I

    aget v0, v0, v2

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->r(I)V

    sget-object v0, Lpmsj/work/a/c;->v:[I

    const/4 v1, 0x3

    aget v0, v0, v1

    invoke-direct {p0, v0}, Lpmsj/work/b/v;->b(I)V

    :goto_0
    return-void

    :cond_0
    sget-object v0, Lpmsj/work/a/c;->v:[I

    const/4 v1, 0x0

    aget v0, v0, v1

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->r(I)V

    sget-object v0, Lpmsj/work/a/c;->v:[I

    aget v0, v0, v2

    invoke-direct {p0, v0}, Lpmsj/work/b/v;->b(I)V

    goto :goto_0
.end method

.method public Q()V
    .locals 2

    const/16 v0, 0x17

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    const/16 v1, 0x2bc

    if-ge v0, v1, :cond_0

    const/4 v0, 0x0

    iput v0, p0, Lpmsj/work/b/v;->s:I

    :goto_0
    return-void

    :cond_0
    const/16 v1, 0x320

    if-ge v0, v1, :cond_1

    const/high16 v0, 0x990000

    iput v0, p0, Lpmsj/work/b/v;->s:I

    goto :goto_0

    :cond_1
    const/16 v1, 0x384

    if-ge v0, v1, :cond_2

    sget v0, Lpmsj/work/a/c;->A:I

    iput v0, p0, Lpmsj/work/b/v;->s:I

    goto :goto_0

    :cond_2
    sget v0, Lpmsj/work/a/c;->y:I

    iput v0, p0, Lpmsj/work/b/v;->s:I

    goto :goto_0
.end method

.method public final R()Ljava/lang/String;
    .locals 1

    const/16 v0, 0x27

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/v;->u(I)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public final S()I
    .locals 1

    const/16 v0, 0x9

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public final T()I
    .locals 1

    const/16 v0, 0xc

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public final U()Ljava/lang/String;
    .locals 1

    const/16 v0, 0xc

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/v;->v(I)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public final V()I
    .locals 1

    const/16 v0, 0x17

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public final W()I
    .locals 1

    const/16 v0, 0x15

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public final X()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v0}, Lpmsj/work/b/u;->G()V

    const/4 v0, 0x0

    iput-object v0, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->w()V

    :cond_0
    return-void
.end method

.method public final Y()Z
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    const/high16 v1, 0x200000

    and-int/2addr v1, v0

    if-nez v1, :cond_0

    and-int/lit8 v0, v0, 0x40

    if-eqz v0, :cond_1

    :cond_0
    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_1
    move v0, v2

    goto :goto_0
.end method

.method public final Z()Z
    .locals 2

    const/4 v1, 0x0

    invoke-virtual {p0, v1}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    and-int/lit8 v0, v0, 0x40

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    move v0, v1

    goto :goto_0
.end method

.method public final a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/b/m;)V
    .locals 9

    const v3, 0x57c148

    const/4 v8, 0x1

    iget-short v0, p0, Lpmsj/work/b/v;->w:S

    iget-short v1, p0, Lpmsj/work/b/v;->x:S

    invoke-virtual {p0, p1, v0, v1}, Lpmsj/work/b/v;->c(Ljavax/microedition/lcdui/Graphics;II)V

    invoke-super {p0, p1, p2}, Lpmsj/work/b/n;->a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/b/m;)V

    iget-short v0, p0, Lpmsj/work/b/v;->x:S

    invoke-virtual {p0}, Lpmsj/work/b/v;->t()I

    move-result v1

    sub-int/2addr v0, v1

    iget v1, p0, Lpmsj/work/b/v;->h:I

    sub-int v7, v0, v1

    sget v0, Lpmsj/work/main/k;->d:I

    and-int/lit8 v0, v0, 0x1

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    if-ne p0, v0, :cond_6

    :cond_0
    iget-short v0, p0, Lpmsj/work/b/v;->w:S

    iget-short v1, p0, Lpmsj/work/b/v;->x:S

    invoke-virtual {p0, p1, v0, v1}, Lpmsj/work/b/v;->a(Ljavax/microedition/lcdui/Graphics;II)V

    iget-short v0, p0, Lpmsj/work/b/v;->w:S

    const/16 v1, 0x18

    invoke-virtual {p0, v1}, Lpmsj/work/b/v;->f(B)I

    move-result v1

    iput v1, p0, Lpmsj/work/b/v;->O:I

    iget v1, p0, Lpmsj/work/b/v;->O:I

    if-lez v1, :cond_3

    iget v1, p0, Lpmsj/work/b/v;->O:I

    if-ne v1, v8, :cond_a

    sget-object v1, Lpmsj/work/b/v;->L:Lpmsj/work/a/i;

    if-nez v1, :cond_1

    new-instance v1, Lpmsj/work/a/i;

    iget v2, p0, Lpmsj/work/b/v;->O:I

    sub-int/2addr v2, v8

    invoke-direct {v1, v3, v2}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v1, Lpmsj/work/b/v;->L:Lpmsj/work/a/i;

    :cond_1
    sget-object v1, Lpmsj/work/b/v;->L:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/b/v;->K:Lpmsj/work/a/i;

    :cond_2
    :goto_0
    iget-object v1, p0, Lpmsj/work/b/v;->K:Lpmsj/work/a/i;

    if-eqz v1, :cond_3

    invoke-virtual {p0}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v1

    invoke-direct {p0, v1}, Lpmsj/work/b/v;->a(Ljava/lang/String;)I

    move-result v1

    div-int/lit8 v1, v1, 0x2

    add-int/2addr v0, v1

    add-int/lit8 v0, v0, 0x4

    iget-object v1, p0, Lpmsj/work/b/v;->K:Lpmsj/work/a/i;

    invoke-virtual {v1, p1, v0, v7}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_3
    iget-short v0, p0, Lpmsj/work/b/v;->w:S

    const/16 v1, 0x15

    invoke-virtual {p0, v1}, Lpmsj/work/b/v;->f(B)I

    move-result v1

    invoke-static {v1}, Lpmsj/work/b/v;->w(I)Ljava/lang/String;

    move-result-object v1

    const-string v2, ""

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_6

    iget-object v2, p0, Lpmsj/work/b/v;->i:Ljava/lang/StringBuffer;

    if-nez v2, :cond_4

    new-instance v2, Ljava/lang/StringBuffer;

    invoke-direct {v2}, Ljava/lang/StringBuffer;-><init>()V

    iput-object v2, p0, Lpmsj/work/b/v;->i:Ljava/lang/StringBuffer;

    :cond_4
    iget-object v2, p0, Lpmsj/work/b/v;->i:Ljava/lang/StringBuffer;

    const/4 v3, 0x0

    invoke-virtual {v2, v3}, Ljava/lang/StringBuffer;->setLength(I)V

    iget-object v2, p0, Lpmsj/work/b/v;->i:Ljava/lang/StringBuffer;

    const-string v3, "["

    invoke-virtual {v2, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v2, p0, Lpmsj/work/b/v;->i:Ljava/lang/StringBuffer;

    const/16 v3, 0xa

    invoke-virtual {p0, v3}, Lpmsj/work/b/v;->j(B)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v2, p0, Lpmsj/work/b/v;->i:Ljava/lang/StringBuffer;

    const-string v3, "]"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v2, p0, Lpmsj/work/b/v;->i:Ljava/lang/StringBuffer;

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v1, p0, Lpmsj/work/b/v;->i:Ljava/lang/StringBuffer;

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    iget-object v2, p0, Lpmsj/work/b/v;->R:Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_5

    iput-object v1, p0, Lpmsj/work/b/v;->R:Ljava/lang/String;

    sget-object v2, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v2, v1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v2

    iput v2, p0, Lpmsj/work/b/v;->S:I

    :cond_5
    iget v2, p0, Lpmsj/work/b/v;->S:I

    div-int/lit8 v2, v2, 0x2

    sub-int v2, v0, v2

    iget v0, p0, Lpmsj/work/b/v;->h:I

    sub-int v3, v7, v0

    sget-object v4, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    iget v5, p0, Lpmsj/work/b/v;->F:I

    iget v6, p0, Lpmsj/work/b/v;->G:I

    move-object v0, p1

    invoke-static/range {v0 .. v6}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;IILjavax/microedition/lcdui/Font;II)V

    :cond_6
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->g()Lpmsj/work/b/n;

    move-result-object v0

    if-ne v0, p0, :cond_7

    invoke-virtual {p0}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v1

    iget-short v0, p0, Lpmsj/work/b/v;->w:S

    invoke-virtual {p0}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v2

    invoke-direct {p0, v2}, Lpmsj/work/b/v;->a(Ljava/lang/String;)I

    move-result v2

    shr-int/lit8 v2, v2, 0x1

    sub-int v2, v0, v2

    sget-object v4, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    sget v5, Lpmsj/work/a/c;->G:I

    iget v6, p0, Lpmsj/work/b/v;->t:I

    move-object v0, p1

    move v3, v7

    invoke-static/range {v0 .. v6}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;IILjavax/microedition/lcdui/Font;II)V

    :cond_7
    const/16 v0, 0x8

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->a(I)Z

    move-result v0

    if-eqz v0, :cond_8

    const/16 v0, 0xd

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->j(B)Ljava/lang/String;

    move-result-object v0

    sget-object v1, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v1, v0}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v1

    iget-short v2, p0, Lpmsj/work/b/v;->w:S

    div-int/lit8 v3, v1, 0x2

    sub-int/2addr v2, v3

    iget v3, p0, Lpmsj/work/b/v;->h:I

    sub-int v3, v7, v3

    sub-int v4, v2, v8

    add-int/lit8 v5, v1, 0x2

    iget v6, p0, Lpmsj/work/b/v;->h:I

    add-int/lit8 v6, v6, 0x1

    invoke-static {p1, v4, v3, v5, v6}, La/a/f;->a(Ljavax/microedition/lcdui/Graphics;IIII)V

    sget v4, Lpmsj/work/a/c;->U:I

    invoke-virtual {p1, v4}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    sub-int v4, v2, v8

    add-int/lit8 v1, v1, 0x2

    iget v5, p0, Lpmsj/work/b/v;->h:I

    add-int/lit8 v5, v5, 0x1

    invoke-virtual {p1, v4, v3, v1, v5}, Ljavax/microedition/lcdui/Graphics;->b(IIII)V

    invoke-static {p1, v0, v2, v3}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;II)V

    :cond_8
    const/16 v0, 0x40

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->a(I)Z

    move-result v0

    if-eqz v0, :cond_9

    iget-short v0, p0, Lpmsj/work/b/v;->w:S

    invoke-virtual {p0}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v1

    invoke-direct {p0, v1}, Lpmsj/work/b/v;->a(Ljava/lang/String;)I

    move-result v1

    shr-int/lit8 v1, v1, 0x1

    sub-int/2addr v0, v1

    sub-int/2addr v0, v8

    invoke-virtual {p0, p1, v0, v7}, Lpmsj/work/b/v;->e(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_9
    iget-short v0, p0, Lpmsj/work/b/v;->w:S

    iget-short v1, p0, Lpmsj/work/b/v;->x:S

    invoke-virtual {p0, p1, v0, v1}, Lpmsj/work/b/v;->d(Ljavax/microedition/lcdui/Graphics;II)V

    return-void

    :cond_a
    iget v1, p0, Lpmsj/work/b/v;->O:I

    const/4 v2, 0x2

    if-ne v1, v2, :cond_c

    sget-object v1, Lpmsj/work/b/v;->M:Lpmsj/work/a/i;

    if-nez v1, :cond_b

    new-instance v1, Lpmsj/work/a/i;

    iget v2, p0, Lpmsj/work/b/v;->O:I

    sub-int/2addr v2, v8

    invoke-direct {v1, v3, v2}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v1, Lpmsj/work/b/v;->M:Lpmsj/work/a/i;

    :cond_b
    sget-object v1, Lpmsj/work/b/v;->M:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/b/v;->K:Lpmsj/work/a/i;

    goto/16 :goto_0

    :cond_c
    iget v1, p0, Lpmsj/work/b/v;->O:I

    const/4 v2, 0x3

    if-ne v1, v2, :cond_2

    sget-object v1, Lpmsj/work/b/v;->N:Lpmsj/work/a/i;

    if-nez v1, :cond_d

    new-instance v1, Lpmsj/work/a/i;

    iget v2, p0, Lpmsj/work/b/v;->O:I

    sub-int/2addr v2, v8

    invoke-direct {v1, v3, v2}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v1, Lpmsj/work/b/v;->N:Lpmsj/work/a/i;

    :cond_d
    sget-object v1, Lpmsj/work/b/v;->N:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/b/v;->K:Lpmsj/work/a/i;

    goto/16 :goto_0
.end method

.method public final a(Lpmsj/work/b/n;)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    return-void
.end method

.method public a(I)Z
    .locals 2

    const/4 v1, 0x0

    invoke-virtual {p0, v1}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    and-int/2addr v0, p1

    if-ne v0, p1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    move v0, v1

    goto :goto_0
.end method

.method public final aa()Z
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    const/high16 v1, 0x200000

    and-int/2addr v0, v1

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    move v0, v2

    goto :goto_0
.end method

.method public final ab()Z
    .locals 1

    invoke-virtual {p0}, Lpmsj/work/b/v;->Z()Z

    move-result v0

    if-eqz v0, :cond_0

    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_0
    invoke-virtual {p0}, Lpmsj/work/b/v;->u()I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/aa;->h(I)Z

    move-result v0

    goto :goto_0
.end method

.method public final ac()Z
    .locals 2

    const/16 v0, 0xc

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    const/4 v1, 0x2

    if-eq v1, v0, :cond_0

    const/4 v1, 0x6

    if-ne v1, v0, :cond_1

    :cond_0
    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_1
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final ad()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    iput-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    return-void
.end method

.method public final ae()V
    .locals 4

    const/4 v3, 0x1

    iget-object v0, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->w()V

    iget-byte v0, p0, Lpmsj/work/b/v;->e:B

    sub-int/2addr v0, v3

    iget-byte v1, p0, Lpmsj/work/b/v;->f:B

    sub-int/2addr v1, v3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_1

    iget-object v2, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/u;->c(II)V

    goto :goto_0

    :cond_1
    iget-byte v0, p0, Lpmsj/work/b/v;->e:B

    sub-int/2addr v0, v3

    iget-byte v1, p0, Lpmsj/work/b/v;->f:B

    add-int/lit8 v1, v1, 0x1

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_2

    iget-object v2, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/u;->c(II)V

    goto :goto_0

    :cond_2
    iget-byte v0, p0, Lpmsj/work/b/v;->e:B

    add-int/lit8 v0, v0, 0x1

    iget-byte v1, p0, Lpmsj/work/b/v;->f:B

    sub-int/2addr v1, v3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_3

    iget-object v2, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/u;->c(II)V

    goto :goto_0

    :cond_3
    iget-byte v0, p0, Lpmsj/work/b/v;->e:B

    add-int/lit8 v0, v0, 0x1

    iget-byte v1, p0, Lpmsj/work/b/v;->f:B

    add-int/lit8 v1, v1, 0x1

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_4

    iget-object v2, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/u;->c(II)V

    goto :goto_0

    :cond_4
    iget-object v0, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    iget-byte v1, p0, Lpmsj/work/b/v;->e:B

    iget-byte v2, p0, Lpmsj/work/b/v;->f:B

    invoke-virtual {v0, v1, v2}, Lpmsj/work/b/u;->c(II)V

    goto :goto_0
.end method

.method public final af()Z
    .locals 3

    const/4 v0, -0x1

    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/b/v;->j(B)Ljava/lang/String;

    move-result-object v1

    const-string v2, "[GM]"

    invoke-virtual {v1, v2}, Ljava/lang/String;->indexOf(Ljava/lang/String;)I

    move-result v1

    if-eq v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final b(IIZ)I
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    invoke-virtual {v0}, Lpmsj/work/b/n;->M()Z

    move-result v0

    if-nez v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->J:Lpmsj/work/b/n;

    iget-byte v1, p0, Lpmsj/work/b/v;->e:B

    iget-byte v2, p0, Lpmsj/work/b/v;->f:B

    invoke-virtual {v0, v1, v2, p3}, Lpmsj/work/b/n;->b(IIZ)I

    :cond_0
    invoke-super {p0, p1, p2, p3}, Lpmsj/work/b/n;->b(IIZ)I

    move-result v0

    return v0
.end method

.method public c()I
    .locals 1

    const/16 v0, 0xb

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public d(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    if-nez p1, :cond_1

    invoke-virtual {p0}, Lpmsj/work/b/v;->q()Z

    move-result v0

    if-eqz v0, :cond_1

    const/4 v0, 0x1

    :goto_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v2, 0x3

    add-int/lit16 v0, v0, 0x36b0

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0

    :cond_1
    move v0, p1

    goto :goto_1
.end method

.method public e(I)V
    .locals 5

    const/4 v4, 0x0

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    div-int/lit8 v0, p1, 0xa

    move v1, v4

    :goto_1
    const/16 v2, 0x8

    if-ge v1, v2, :cond_1

    iget-object v2, p0, Lpmsj/work/b/v;->o:La/a/d;

    add-int/lit8 v3, v1, 0xb

    invoke-virtual {v2, v3, v4}, La/a/d;->a(II)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_1

    :cond_1
    if-nez v0, :cond_2

    invoke-virtual {p0, v4}, Lpmsj/work/b/v;->e(B)V

    :goto_2
    move v1, v4

    :goto_3
    const/16 v2, 0xd

    if-ge v1, v2, :cond_3

    iget-object v2, p0, Lpmsj/work/b/v;->o:La/a/d;

    add-int/lit8 v3, v1, 0x13

    invoke-virtual {v2, v3, v4}, La/a/d;->a(II)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_3

    :cond_2
    invoke-static {v0}, Lpmsj/work/b/v;->K(I)I

    move-result v1

    iget-object v2, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v2, v1, v0}, La/a/d;->a(II)V

    invoke-static {v0}, Lpmsj/work/b/v;->K(I)I

    move-result v1

    packed-switch v1, :pswitch_data_0

    move v1, v4

    :goto_4
    invoke-virtual {p0, v1}, Lpmsj/work/b/v;->e(B)V

    goto :goto_2

    :pswitch_0
    const/4 v1, 0x1

    goto :goto_4

    :pswitch_1
    const/4 v1, 0x2

    goto :goto_4

    :pswitch_2
    const/4 v1, 0x3

    goto :goto_4

    :pswitch_3
    const/4 v1, 0x4

    goto :goto_4

    :cond_3
    rem-int/lit8 v1, p1, 0xa

    if-eqz v1, :cond_4

    div-int/lit8 v0, v0, 0x64

    move v2, v4

    :goto_5
    sget-object v3, Lpmsj/work/b/v;->I:[S

    array-length v3, v3

    if-ge v2, v3, :cond_6

    sget-object v3, Lpmsj/work/b/v;->I:[S

    aget-short v3, v3, v2

    if-ne v0, v3, :cond_5

    add-int/lit8 v0, v2, 0x13

    :goto_6
    if-eqz v0, :cond_4

    const/16 v2, 0x13

    sub-int v2, v0, v2

    mul-int/lit8 v2, v2, 0x64

    add-int/lit16 v2, v2, 0x7530

    add-int/2addr v1, v2

    iget-object v2, p0, Lpmsj/work/b/v;->o:La/a/d;

    invoke-virtual {v2, v0, v1}, La/a/d;->a(II)V

    :cond_4
    invoke-virtual {p0}, Lpmsj/work/b/v;->N()V

    goto :goto_0

    :cond_5
    add-int/lit8 v2, v2, 0x1

    goto :goto_5

    :cond_6
    move v0, v4

    goto :goto_6

    nop

    :pswitch_data_0
    .packed-switch 0xb
        :pswitch_0
        :pswitch_3
        :pswitch_0
        :pswitch_2
        :pswitch_0
        :pswitch_2
        :pswitch_1
        :pswitch_0
    .end packed-switch
.end method

.method protected e(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 4

    iget-object v0, p0, Lpmsj/work/b/v;->A:Lpmsj/work/a/b;

    if-nez v0, :cond_0

    new-instance v0, Lpmsj/work/a/b;

    const v1, 0x561590

    invoke-direct {v0, v1}, Lpmsj/work/a/b;-><init>(I)V

    iput-object v0, p0, Lpmsj/work/b/v;->A:Lpmsj/work/a/b;

    :cond_0
    iget-object v0, p0, Lpmsj/work/b/v;->A:Lpmsj/work/a/b;

    iget-object v1, p0, Lpmsj/work/b/v;->A:Lpmsj/work/a/b;

    invoke-virtual {v1}, Lpmsj/work/a/b;->c()I

    move-result v1

    sub-int v1, p2, v1

    iget v2, p0, Lpmsj/work/b/v;->h:I

    iget-object v3, p0, Lpmsj/work/b/v;->A:Lpmsj/work/a/b;

    invoke-virtual {v3}, Lpmsj/work/a/b;->b()I

    move-result v3

    sub-int/2addr v2, v3

    shr-int/lit8 v2, v2, 0x1

    add-int/2addr v2, p3

    invoke-virtual {v0, p1, v1, v2}, Lpmsj/work/a/b;->a(Ljavax/microedition/lcdui/Graphics;II)V

    return-void
.end method

.method public h(II)V
    .locals 1

    invoke-virtual {p0, p1, p2}, Lpmsj/work/b/v;->c(II)V

    invoke-virtual {p0}, Lpmsj/work/b/v;->D()V

    iget-object v0, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v0}, Lpmsj/work/b/u;->D()V

    :cond_0
    return-void
.end method

.method public p()Ljava/lang/String;
    .locals 1

    const/4 v0, 0x3

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->j(B)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public q()Z
    .locals 2

    const/4 v1, 0x1

    const/4 v0, 0x6

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    rem-int/lit8 v0, v0, 0x2

    int-to-byte v0, v0

    if-ne v1, v0, :cond_0

    move v0, v1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public r()V
    .locals 2

    const/4 v1, 0x6

    invoke-virtual {p0, v1}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->M(I)V

    invoke-virtual {p0, v1}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->y(I)V

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->d(I)V

    const/16 v0, 0xe

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->z(I)V

    const/16 v0, 0xf

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->A(I)V

    const/16 v0, 0x10

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->B(I)V

    const/16 v0, 0x11

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->C(I)V

    const/16 v0, 0x12

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->D(I)V

    const/16 v0, 0x13

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->E(I)V

    const/16 v0, 0x14

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->F(I)V

    const/4 v0, 0x7

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->e(I)V

    const/16 v0, 0x16

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->G(I)V

    const/16 v0, 0x1a

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->J(I)V

    return-void
.end method

.method public w()I
    .locals 1

    const/16 v0, 0x28

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public final x()I
    .locals 1

    const/16 v0, 0x29

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public y()I
    .locals 1

    const/16 v0, 0x2a

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public final y(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v1, 0x0

    add-int/lit16 v2, p1, 0x2af8

    invoke-virtual {v0, v1, v2}, La/a/d;->a(II)V

    goto :goto_0
.end method

.method public final z()I
    .locals 1

    const/16 v0, 0x2b

    invoke-virtual {p0, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    return v0
.end method

.method public final z(I)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/b/v;->o:La/a/d;

    if-nez v0, :cond_0

    :goto_0
    return-void

    :cond_0
    if-nez p1, :cond_1

    invoke-virtual {p0}, Lpmsj/work/b/v;->q()Z

    move-result v0

    if-eqz v0, :cond_1

    const/4 v0, 0x1

    :goto_1
    iget-object v1, p0, Lpmsj/work/b/v;->o:La/a/d;

    const/4 v2, 0x4

    add-int/lit16 v0, v0, 0x3a98

    invoke-virtual {v1, v2, v0}, La/a/d;->a(II)V

    goto :goto_0

    :cond_1
    move v0, p1

    goto :goto_1
.end method
